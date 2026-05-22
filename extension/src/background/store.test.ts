import { beforeEach, describe, expect, test } from "bun:test";
import type { PersistedCredential, Settings } from "@/types/messages";
import { deterministicBase64Url, createChromeStorageMock } from "./test-utils";
import { getSettings, listCredentials, saveSettings, upsertCredential } from "./store";

const SETTINGS_KEY = "pq_settings_v1";
const LEGACY_CREDENTIALS_KEY = "pq_credentials_v1";

const SAMPLE_RECORD: PersistedCredential = {
  credentialId: deterministicBase64Url("cred-1", 32),
  rpId: "demo.yubico.com",
  userHandle: deterministicBase64Url("user-1", 16),
  publicKey: deterministicBase64Url("pub-1", 1312),
  privateKey: deterministicBase64Url("priv-1", 2560),
  algorithm: -48,
  signCount: 0,
  createdAt: "2026-02-08T00:00:00.000Z"
};

describe("store", () => {
  beforeEach(() => {
    (globalThis as unknown as { chrome: unknown }).chrome = createChromeStorageMock();
  });

  test("returns default settings when empty", async () => {
    const settings = await getSettings();
    expect(settings.enabled).toBe(true);
    expect(settings.defaultAlgorithm).toBe(-48);
    expect(settings.uvMode).toBe("soft-auto");
  });

  test("saves and loads settings", async () => {
    const next: Settings = {
      enabled: false,
      defaultAlgorithm: -49,
      uvMode: "soft-auto"
    };
    await saveSettings(next);
    const loaded = await getSettings();
    expect(loaded).toEqual(next);
  });

  test("upsert inserts and updates credential", async () => {
    await upsertCredential(SAMPLE_RECORD);
    let credentials = await listCredentials();
    expect(credentials).toHaveLength(1);
    expect(credentials[0].signCount).toBe(0);

    await upsertCredential({ ...SAMPLE_RECORD, signCount: 2 });
    credentials = await listCredentials();
    expect(credentials).toHaveLength(1);
    expect(credentials[0].signCount).toBe(2);
  });

  test("migrates from legacy credential key", async () => {
    const chromeMock = createChromeStorageMock({
      [LEGACY_CREDENTIALS_KEY]: [SAMPLE_RECORD],
      [SETTINGS_KEY]: { enabled: true }
    });
    (globalThis as unknown as { chrome: unknown }).chrome = chromeMock;

    const credentials = await listCredentials();
    expect(credentials).toHaveLength(1);
    expect(credentials[0].credentialId).toBe(SAMPLE_RECORD.credentialId);
  });
});
