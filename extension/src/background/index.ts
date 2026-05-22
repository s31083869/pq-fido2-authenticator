import { PQAuthenticator, WebAuthnError } from "./authenticator";
import { checkNativeUvHostStatus, type NativeUvMode } from "./native-uv";
import { getSettings, saveSettings } from "./store";
import type { BridgeRequestMessage, BridgeResponseMessage, Settings } from "@/types/messages";

const authenticator = new PQAuthenticator();

interface UvStatusRequestMessage {
  channel: "PQ_UV_STATUS";
  action: "check";
  mode?: NativeUvMode;
}

async function ensureDefaultSettings(): Promise<void> {
  const settings = await getSettings();
  await saveSettings(settings);
}

function isTrustedSender(sender: chrome.runtime.MessageSender): boolean {
  const url = sender.url ?? sender.tab?.url;
  if (!url) {
    return false;
  }
  try {
    const parsed = new URL(url);
    return parsed.hostname === "demo.yubico.com";
  } catch {
    return false;
  }
}

function isExtensionSender(sender: chrome.runtime.MessageSender): boolean {
  return sender.id === chrome.runtime.id;
}

function normalizeError(error: unknown): BridgeResponseMessage {
  if (error instanceof WebAuthnError) {
    return {
      ok: false,
      error: {
        name: error.name,
        message: error.message
      }
    };
  }

  if (error instanceof Error) {
    return {
      ok: false,
      error: {
        name: error.name || "Error",
        message: error.message
      }
    };
  }

  return {
    ok: false,
    error: {
      name: "Error",
      message: "Unknown extension error"
    }
  };
}

async function handleNativeUvStatus(mode?: NativeUvMode) {
  const status = await checkNativeUvHostStatus(mode);
  return {
    ok: true as const,
    result: status
  };
}

function isUvStatusRequest(message: unknown): message is UvStatusRequestMessage {
  if (!message || typeof message !== "object") {
    return false;
  }
  const record = message as Record<string, unknown>;
  return record.channel === "PQ_UV_STATUS" && record.action === "check";
}

function isBridgeRequest(message: unknown): message is BridgeRequestMessage {
  if (!message || typeof message !== "object") {
    return false;
  }
  const record = message as Record<string, unknown>;
  return record.channel === "PQ_WEBAUTHN_BRIDGE";
}

async function handleMessage(message: BridgeRequestMessage): Promise<BridgeResponseMessage> {
  const settings: Settings = await getSettings();

  if (message.action === "create") {
    const result = await authenticator.makeCredential(message.payload, settings);
    return { ok: true, result };
  }

  const result = await authenticator.getAssertion(message.payload, settings);
  return { ok: true, result };
}

chrome.runtime.onInstalled.addListener(() => {
  void ensureDefaultSettings();
});

chrome.runtime.onMessage.addListener((message: unknown, sender, sendResponse) => {
  if (isUvStatusRequest(message)) {
    if (!isExtensionSender(sender)) {
      sendResponse({
        ok: false,
        error: {
          name: "SecurityError",
          message: "Only extension pages can request UV host status"
        }
      });
      return;
    }
    void handleNativeUvStatus(message.mode)
      .then(sendResponse)
      .catch((error) => sendResponse(normalizeError(error)));
    return true;
  }

  if (!isBridgeRequest(message)) {
    return;
  }

  if (!isTrustedSender(sender)) {
    sendResponse({
      ok: false,
      error: {
        name: "SecurityError",
        message: "Sender origin is not allowed"
      }
    } satisfies BridgeResponseMessage);
    return;
  }

  void handleMessage(message)
    .then(sendResponse)
    .catch((error) => sendResponse(normalizeError(error)));

  return true;
});
