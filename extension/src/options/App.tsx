import { useEffect, useState } from "react";
import type { Settings, SupportedAlg } from "@/types/messages";

const SETTINGS_KEY = "pq_settings_v1";

const DEFAULT_SETTINGS: Settings = {
  enabled: true,
  defaultAlgorithm: -48,
  uvMode: "soft-auto"
};

function isNativeUvMode(uvMode: Settings["uvMode"]): boolean {
  return uvMode === "native-touch-id" || uvMode === "native-windows-hello";
}

interface NativeUvStatusResult {
  ready: boolean;
  host: string;
  version?: string;
  platform?: string;
  detail: string;
}

interface NativeUvStatusState {
  loading: boolean;
  ready: boolean | null;
  detail: string;
  version?: string;
  platform?: string;
}

function App() {
  const [settings, setSettings] = useState<Settings>(DEFAULT_SETTINGS);
  const [saved, setSaved] = useState(false);
  const [nativeUvStatus, setNativeUvStatus] = useState<NativeUvStatusState>({
    loading: false,
    ready: null,
    detail: "尚未檢查"
  });

  useEffect(() => {
    chrome.storage.local.get(SETTINGS_KEY).then((result) => {
      setSettings({
        ...DEFAULT_SETTINGS,
        ...(result[SETTINGS_KEY] ?? {})
      });
    });
  }, []);

  const updateSetting = <K extends keyof Settings>(key: K, value: Settings[K]) => {
    setSaved(false);
    setSettings((prev) => ({ ...prev, [key]: value }));
  };

  const refreshNativeUvStatus = () => {
    setNativeUvStatus((prev) => ({ ...prev, loading: true }));
    chrome.runtime.sendMessage(
      {
        channel: "PQ_UV_STATUS",
        action: "check",
        mode: settings.uvMode
      },
      (response?: {
        ok?: boolean;
        result?: NativeUvStatusResult;
        error?: { message?: string };
      }) => {
        const runtimeError = chrome.runtime.lastError?.message;
        if (runtimeError) {
          setNativeUvStatus({
            loading: false,
            ready: false,
            detail: runtimeError
          });
          return;
        }
        if (!response?.ok || !response.result) {
          setNativeUvStatus({
            loading: false,
            ready: false,
            detail: response?.error?.message ?? "無法取得 native host 狀態"
          });
          return;
        }
        setNativeUvStatus({
          loading: false,
          ready: response.result.ready,
          detail: response.result.detail,
          version: response.result.version,
          platform: response.result.platform
        });
      }
    );
  };

  useEffect(() => {
    if (isNativeUvMode(settings.uvMode)) {
      refreshNativeUvStatus();
    }
  }, [settings.uvMode]);

  const onSave = async () => {
    await chrome.storage.local.set({ [SETTINGS_KEY]: settings });
    setSaved(true);
  };

  return (
    <main className="min-h-screen bg-slate-50 text-slate-900">
      <div className="mx-auto max-w-2xl space-y-6 p-8">
        <h1 className="text-2xl font-semibold">PQ WebAuthn Extension Settings</h1>

        <section className="space-y-4 rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
          <label className="flex items-center justify-between">
            <span className="font-medium">Enable hook on demo.yubico.com</span>
            <input
              type="checkbox"
              checked={settings.enabled}
              onChange={(event) => updateSetting("enabled", event.target.checked)}
            />
          </label>

          <label className="block">
            <span className="mb-1 block font-medium">Default algorithm</span>
            <select
              className="w-full rounded border border-slate-300 px-3 py-2"
              value={String(settings.defaultAlgorithm)}
              onChange={(event) =>
                updateSetting("defaultAlgorithm", Number(event.target.value) as SupportedAlg)
              }
            >
              <option value="-48">ML-DSA-44 (-48)</option>
              <option value="-49">ML-DSA-65 (-49)</option>
              <option value="-50">ML-DSA-87 (-50)</option>
            </select>
          </label>

          <label className="block">
            <span className="mb-1 block font-medium">UV mode</span>
            <select
              className="w-full rounded border border-slate-300 px-3 py-2"
              value={settings.uvMode}
              onChange={(event) => updateSetting("uvMode", event.target.value as Settings["uvMode"])}
            >
              <option value="soft-auto">soft-auto (trial)</option>
              <option value="native-touch-id">native-touch-id (macOS Touch ID)</option>
              <option value="native-windows-hello">native-windows-hello (Windows Hello)</option>
            </select>
          </label>

          {isNativeUvMode(settings.uvMode) ? (
            <div className="rounded border border-slate-200 bg-slate-50 p-3 text-sm">
              <div className="flex items-center justify-between">
                <span className="font-medium">Native host status</span>
                <button
                  type="button"
                  onClick={refreshNativeUvStatus}
                  className="rounded border border-slate-300 px-2 py-1 text-xs hover:bg-slate-100"
                >
                  Refresh
                </button>
              </div>
              <p className="mt-2">
                Status:{" "}
                {nativeUvStatus.loading
                  ? "checking..."
                  : nativeUvStatus.ready
                    ? "ready"
                    : "not ready"}
              </p>
              <p>Detail: {nativeUvStatus.detail}</p>
              {nativeUvStatus.version ? <p>Version: {nativeUvStatus.version}</p> : null}
              {nativeUvStatus.platform ? <p>Platform: {nativeUvStatus.platform}</p> : null}
            </div>
          ) : null}

          <button
            type="button"
            onClick={onSave}
            className="rounded bg-slate-900 px-4 py-2 font-medium text-white hover:bg-slate-700"
          >
            Save settings
          </button>

          {saved ? <p className="text-sm text-emerald-700">Saved.</p> : null}
        </section>
      </div>
    </main>
  );
}

export default App;
