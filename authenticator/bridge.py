"""Playwright bridge that intercepts WebAuthn calls and delegates to the authenticator."""

from __future__ import annotations

import asyncio
import logging
from typing import Any, Dict

from playwright.async_api import BrowserContext, Error as PlaywrightError, Page, async_playwright

from .service import Authenticator

LOGGER = logging.getLogger(__name__)


INJECT_SCRIPT = r"""
(() => {
  const bufferToBase64url = (buffer) => {
    let view;
    if (buffer instanceof ArrayBuffer) {
      view = new Uint8Array(buffer);
    } else if (ArrayBuffer.isView(buffer)) {
      view = new Uint8Array(buffer.buffer, buffer.byteOffset, buffer.byteLength);
    } else {
      throw new Error("Unsupported buffer type");
    }
    let binary = "";
    view.forEach((b) => {
      binary += String.fromCharCode(b);
    });
    return btoa(binary).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
  };

  const base64urlToArrayBuffer = (value) => {
    const padding = "=".repeat((4 - (value.length % 4)) % 4);
    const base64 = (value + padding).replace(/-/g, "+").replace(/_/g, "/");
    const binary = atob(base64);
    const buffer = new ArrayBuffer(binary.length);
    const bytes = new Uint8Array(buffer);
    for (let i = 0; i < binary.length; i += 1) {
      bytes[i] = binary.charCodeAt(i);
    }
    return buffer;
  };

  const serializeDescriptors = (items = []) =>
    items.map((item) => ({
      type: item.type,
      id: bufferToBase64url(item.id),
      transports: item.transports,
    }));

  const serializeCreationOptions = (options) => ({
    rp: options.rp,
    user: {
      ...options.user,
      id: bufferToBase64url(options.user.id),
    },
    challenge: bufferToBase64url(options.challenge),
    pubKeyCredParams: options.pubKeyCredParams?.map((param) => ({ type: param.type, alg: param.alg })) ?? [],
    timeout: options.timeout ?? 90_000,
    attestation: options.attestation ?? "none",
    authenticatorSelection: options.authenticatorSelection ?? {},
    excludeCredentials: serializeDescriptors(options.excludeCredentials ?? []),
    extensions: options.extensions ?? {},
  });

  const serializeRequestOptions = (options) => ({
    rpId: options.rpId,
    challenge: bufferToBase64url(options.challenge),
    allowCredentials: serializeDescriptors(options.allowCredentials ?? []),
    timeout: options.timeout ?? 90_000,
    userVerification: options.userVerification ?? "preferred",
    extensions: options.extensions ?? {},
  });

  const buildAttestationResponse = (response) => {
    const att = {
      clientDataJSON: base64urlToArrayBuffer(response.clientDataJSON),
      attestationObject: base64urlToArrayBuffer(response.attestationObject),
      getAuthenticatorData: () =>
        response.authenticatorData
          ? base64urlToArrayBuffer(response.authenticatorData)
          : new ArrayBuffer(0),
      getPublicKey: () =>
        response.publicKey ? base64urlToArrayBuffer(response.publicKey) : null,
      getPublicKeyAlgorithm: () => response.publicKeyAlgorithm ?? null,
      getTransports: () => response.transports ?? [],
      toJSON: () => response,
    };
    return att;
  };

  const buildAssertionResponse = (response) => {
    const assertion = {
      clientDataJSON: base64urlToArrayBuffer(response.clientDataJSON),
      authenticatorData: base64urlToArrayBuffer(response.authenticatorData),
      signature: base64urlToArrayBuffer(response.signature),
      userHandle: response.userHandle
        ? base64urlToArrayBuffer(response.userHandle)
        : null,
      toJSON: () => response,
    };
    return assertion;
  };

  const buildCredential = (payload) => {
    const response = payload.response || {};
    return {
      id: payload.id,
      rawId: base64urlToArrayBuffer(payload.rawId ?? payload.id),
      type: payload.type ?? "public-key",
      authenticatorAttachment: payload.authenticatorAttachment ?? "platform",
      getClientExtensionResults: () => payload.clientExtensionResults || {},
      response: response.attestationObject
        ? buildAttestationResponse(response)
        : buildAssertionResponse(response),
      toJSON: () => payload,
    };
  };

  const wrapNavigator = () => {
    if (!navigator.credentials || navigator.credentials.__pqHooked) {
      return;
    }
    const originalCreate = navigator.credentials.create.bind(navigator.credentials);
    const originalGet = navigator.credentials.get.bind(navigator.credentials);

    navigator.credentials.create = async (options) => {
      if (!options?.publicKey || typeof window.__pqMakeCredential !== "function") {
        return originalCreate(options);
      }
      const payload = {
        origin: window.location.origin,
        publicKey: serializeCreationOptions(options.publicKey),
      };
      const result = await window.__pqMakeCredential(payload);
      return buildCredential(result);
    };

    navigator.credentials.get = async (options) => {
      if (!options?.publicKey || typeof window.__pqGetAssertion !== "function") {
        return originalGet(options);
      }
      const payload = {
        origin: window.location.origin,
        publicKey: serializeRequestOptions(options.publicKey),
      };
      const result = await window.__pqGetAssertion(payload);
      return buildCredential(result);
    };

    Object.defineProperty(navigator.credentials, "__pqHooked", { value: true });
    console.info("[PQ-Authenticator] navigator.credentials hooked");
  };

  wrapNavigator();
})();
"""


class PlaywrightBridge:
    """Launches Chromium, injects interception scripts, and bridges to Authenticator."""

    def __init__(
        self,
        authenticator: Authenticator,
        target_url: str,
        *,
        headless: bool = False,
    ) -> None:
        self.authenticator = authenticator
        self.target_url = target_url
        self.headless = headless

    async def run(self) -> None:
        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch(headless=self.headless)
            context = await browser.new_context()
            await self._prepare_context(context)
            page = await context.new_page()
            LOGGER.info("[INFO] Opening %s", self.target_url)
            try:
                await page.goto(self.target_url)
            except PlaywrightError as exc:
                LOGGER.error(
                    "[ERROR] Failed to open %s. Make sure the frontend is running "
                    "before starting the authenticator bridge.\n%s",
                    self.target_url,
                    exc,
                )
                raise
            LOGGER.info("[INFO] PQ Authenticator bridge active. Press Ctrl+C to exit.")
            try:
                while True:
                    await asyncio.sleep(3600)
            except asyncio.CancelledError:  # pragma: no cover - manual interruption
                LOGGER.info("Bridge cancelled")
            finally:
                await browser.close()

    async def _prepare_context(self, context: BrowserContext) -> None:
        await context.expose_binding("__pqMakeCredential", self._handle_make)
        await context.expose_binding("__pqGetAssertion", self._handle_get)
        await context.expose_binding("__pqListCredentials", self._handle_list_credentials)
        await context.add_init_script(INJECT_SCRIPT)
        context.on("page", lambda page: asyncio.create_task(self._install_on_page(page)))

    async def _install_on_page(self, page: Page) -> None:
        await page.add_init_script(INJECT_SCRIPT)

    async def _handle_make(self, _source, payload: Dict[str, Any]) -> Dict[str, Any]:
        loop = asyncio.get_running_loop()
        origin = payload.get("origin")
        options = payload.get("publicKey", payload)
        return await loop.run_in_executor(
            None, self.authenticator.make_credential, options, origin
        )

    async def _handle_get(self, _source, payload: Dict[str, Any]) -> Dict[str, Any]:
        loop = asyncio.get_running_loop()
        origin = payload.get("origin")
        options = payload.get("publicKey", payload)
        return await loop.run_in_executor(
            None, self.authenticator.get_assertion, options, origin
        )

    async def _handle_list_credentials(self, _source, _payload: Dict[str, Any] | None = None) -> Dict[str, Any]:
        loop = asyncio.get_running_loop()
        result = await loop.run_in_executor(None, self.authenticator.list_credentials_metadata)
        return {"credentials": result}
