const REQUEST_SOURCE = "PQ_WEBAUTHN_INJECTED";
const RESPONSE_SOURCE = "PQ_WEBAUTHN_CONTENT";
const SETTINGS_KEY = "pq_settings_v1";

function injectMainWorldScript(): void {
  const script = document.createElement("script");
  script.src = chrome.runtime.getURL("injected.js");
  script.type = "module";
  (document.head || document.documentElement).appendChild(script);
  script.remove();
}

function installBridgeListener(): void {
  window.addEventListener("message", (event: MessageEvent) => {
    if (event.source !== window) {
      return;
    }

    const data = event.data;
    if (!data || data.source !== REQUEST_SOURCE || data.kind !== "REQUEST") {
      return;
    }

    chrome.runtime.sendMessage(
      {
        channel: "PQ_WEBAUTHN_BRIDGE",
        requestId: data.requestId,
        action: data.action,
        payload: data.payload
      },
      (response) => {
        const runtimeError = chrome.runtime.lastError;
        if (runtimeError) {
          window.postMessage(
            {
              source: RESPONSE_SOURCE,
              kind: "RESPONSE",
              requestId: data.requestId,
              ok: false,
              error: {
                name: "NetworkError",
                message: runtimeError.message
              }
            },
            window.location.origin
          );
          return;
        }

        window.postMessage(
          {
            source: RESPONSE_SOURCE,
            kind: "RESPONSE",
            requestId: data.requestId,
            ...(response ?? {
              ok: false,
              error: {
                name: "Error",
                message: "No response from background"
              }
            })
          },
          window.location.origin
        );
      }
    );
  });
}

async function shouldEnableHook(): Promise<boolean> {
  const loaded = await chrome.storage.local.get(SETTINGS_KEY);
  return loaded[SETTINGS_KEY]?.enabled ?? true;
}

async function bootstrap(): Promise<void> {
  if (!(await shouldEnableHook())) {
    return;
  }

  installBridgeListener();
  injectMainWorldScript();
}

void bootstrap();
