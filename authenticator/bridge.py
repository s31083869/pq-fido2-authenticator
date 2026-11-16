"""Playwright bridge that intercepts WebAuthn calls and delegates to the authenticator."""

from __future__ import annotations

import asyncio
import logging
from typing import Any, Dict, Optional
from urllib.parse import urlsplit

from playwright.async_api import (
    BrowserContext,
    Error as PlaywrightError,
    Page,
    async_playwright,
)

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

  // 改寫頁面的 navigator.credentials.create()／get()：WebAuthn 請求改交給 Python authenticator，
  // 透過 Playwright 掛上的 binding（__pqMakeCredential、__pqGetAssertion）送出，結果再組回
  // PublicKeyCredential 物件交給頁面。輸入：無（直接修改目前頁面的 navigator）；輸出：無。
  const wrapNavigator = () => {
    // 沒有 WebAuthn API，或這個頁面已經改寫過（同一頁面可能被注入兩次），就不再處理
    if (!navigator.credentials || navigator.credentials.__pqHooked) {
      return;
    }
    // 保留瀏覽器原本的實作，給不是 WebAuthn 的請求使用
    const originalCreate = navigator.credentials.create.bind(navigator.credentials);
    const originalGet = navigator.credentials.get.bind(navigator.credentials);

    // 註冊：把 PublicKeyCredentialCreationOptions 的二進位欄位轉成 base64url 後交給 Python。
    // payload 不帶 origin：bridge 會從呼叫者 frame 的真實網址取出 origin，不採用頁面提供的值。
    navigator.credentials.create = async (options) => {
      // 不是 WebAuthn 請求（例如密碼憑證），或 binding 不存在時，交回瀏覽器原本的實作
      if (!options?.publicKey || typeof window.__pqMakeCredential !== "function") {
        return originalCreate(options);
      }
      const payload = {
        publicKey: serializeCreationOptions(options.publicKey),
      };
      const result = await window.__pqMakeCredential(payload);
      return buildCredential(result);
    };

    // 登入：流程同註冊，選項換成 PublicKeyCredentialRequestOptions，交給 __pqGetAssertion
    navigator.credentials.get = async (options) => {
      if (!options?.publicKey || typeof window.__pqGetAssertion !== "function") {
        return originalGet(options);
      }
      const payload = {
        publicKey: serializeRequestOptions(options.publicKey),
      };
      const result = await window.__pqGetAssertion(payload);
      return buildCredential(result);
    };

    // 標記為已改寫；defineProperty 預設不可修改、不可列舉
    Object.defineProperty(navigator.credentials, "__pqHooked", { value: true });
    console.info("[PQ-Authenticator] navigator.credentials hooked");
  };

  wrapNavigator();
})();
"""


def _origin_from_url(url: Optional[str]) -> Optional[str]:
    """從頁面網址取出 WebAuthn 的 origin：「協定://網域[:埠]」，不含路徑、查詢字串與帳密。

    例如 http://localhost:3000/register?step=2 → http://localhost:3000。
    frame.url 是 Chromium 正規化過的網址：網域已轉成小寫、預設埠（http 的 80、https 的 443）已省略，
    所以對一般的 http(s) 頁面，結果就是瀏覽器算出的 origin。
    已知的例外是 sandbox iframe：瀏覽器把它的 origin 當成不透明的 "null"，但只看網址分辨不出來，
    這裡仍會回傳網址的 origin。

    參數：
        url：呼叫者所在 frame 的網址。

    回傳：
        origin 字串。網址是空的或沒有網域時（例如 about:blank、about:srcdoc、blob: 開頭的網址）
        回傳 None，交給 authenticator 以「Missing origin」拒絕。這類頁面在瀏覽器中會沿用建立它的頁面
        或內層網址的 origin，但只看 frame.url 無法得知是哪一個，所以選擇拒絕，而不是去猜。
    """
    if not url:
        return None
    parts = urlsplit(url)
    if not parts.scheme or not parts.netloc:
        return None
    # netloc 可能帶有「帳號:密碼@」，origin 不包含這一段，只留最後一個 @ 之後的網域與埠
    host_and_port = parts.netloc.rpartition("@")[2]
    return f"{parts.scheme}://{host_and_port}"


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
        await context.expose_binding(
            "__pqListCredentials", self._handle_list_credentials
        )
        await context.add_init_script(INJECT_SCRIPT)
        context.on(
            "page", lambda page: asyncio.create_task(self._install_on_page(page))
        )

    async def _install_on_page(self, page: Page) -> None:
        await page.add_init_script(INJECT_SCRIPT)

    async def _handle_make(
        self, source: Dict[str, Any], payload: Dict[str, Any]
    ) -> Dict[str, Any]:
        """處理頁面的 navigator.credentials.create()（註冊），交給 authenticator 建立憑證。

        origin 取自呼叫者 frame 的真實網址，不採用 payload 裡頁面自稱的 origin：
        WebAuthn §5.8.1 規定 clientDataJSON 的 origin 由瀏覽器依呼叫者的真實來源填入，
        網頁無法指定。bridge 在這裡扮演瀏覽器，若相信頁面自稱的值，惡意網站只要聲稱自己是
        http://localhost:3000，就能替本站建立憑證。

        參數：
            source：Playwright 附上的呼叫者資訊，"frame" 是發出呼叫的 frame。
            payload：頁面傳來的資料，"publicKey" 是序列化後的 PublicKeyCredentialCreationOptions。

        回傳：
            序列化後的 PublicKeyCredential（含 attestationObject），由注入腳本組回憑證物件交給頁面。
        """
        loop = asyncio.get_running_loop()
        origin = _origin_from_url(source["frame"].url)
        options = payload.get("publicKey", payload)
        # make_credential 會等待 Windows Hello 驗證，放到執行緒池執行，避免卡住 Playwright 的事件迴圈
        return await loop.run_in_executor(
            None, self.authenticator.make_credential, options, origin
        )

    async def _handle_get(
        self, source: Dict[str, Any], payload: Dict[str, Any]
    ) -> Dict[str, Any]:
        """處理頁面的 navigator.credentials.get()（登入），交給 authenticator 產生簽章。

        origin 的取法和 _handle_make() 相同，理由也相同：若相信頁面自稱的 origin，
        惡意網站就能取得本站憑證的簽章，拿去冒充使用者登入。

        參數：
            source：Playwright 附上的呼叫者資訊，"frame" 是發出呼叫的 frame。
            payload：頁面傳來的資料，"publicKey" 是序列化後的 PublicKeyCredentialRequestOptions。

        回傳：
            序列化後的 PublicKeyCredential（含 authenticatorData 與 signature），由注入腳本組回憑證物件交給頁面。
        """
        loop = asyncio.get_running_loop()
        origin = _origin_from_url(source["frame"].url)
        options = payload.get("publicKey", payload)
        # get_assertion 會等待 Windows Hello 驗證，放到執行緒池執行，避免卡住 Playwright 的事件迴圈
        return await loop.run_in_executor(
            None, self.authenticator.get_assertion, options, origin
        )

    async def _handle_list_credentials(
        self, _source, _payload: Dict[str, Any] | None = None
    ) -> Dict[str, Any]:
        loop = asyncio.get_running_loop()
        result = await loop.run_in_executor(
            None, self.authenticator.list_credentials_metadata
        )
        return {"credentials": result}
