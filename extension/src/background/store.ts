import type { PersistedCredential, Settings } from "@/types/messages";

const CREDENTIALS_KEY = "pq_credentials_v1";
const STORE_KEY = "pq_store_v1";
const SETTINGS_KEY = "pq_settings_v1";
const STORE_SCHEMA_VERSION = 1;

const DEFAULT_SETTINGS: Settings = {
  enabled: true,
  defaultAlgorithm: -48,
  uvMode: "soft-auto"
};

interface PersistedStoreV1 {
  schemaVersion: 1;
  credentials: PersistedCredential[];
}

function isPersistedCredential(value: unknown): value is PersistedCredential {
  if (!value || typeof value !== "object") {
    return false;
  }
  const record = value as Record<string, unknown>;
  return (
    typeof record.credentialId === "string" &&
    typeof record.rpId === "string" &&
    typeof record.userHandle === "string" &&
    typeof record.publicKey === "string" &&
    typeof record.privateKey === "string" &&
    typeof record.algorithm === "number" &&
    typeof record.signCount === "number" &&
    typeof record.createdAt === "string"
  );
}

function sanitizeCredentials(input: unknown): PersistedCredential[] {
  if (!Array.isArray(input)) {
    return [];
  }
  return input.filter(isPersistedCredential);
}

async function loadStore(): Promise<PersistedStoreV1> {
  const loaded = await chrome.storage.local.get([STORE_KEY, CREDENTIALS_KEY]);
  const current = loaded[STORE_KEY] as PersistedStoreV1 | undefined;
  if (
    current &&
    typeof current === "object" &&
    current.schemaVersion === STORE_SCHEMA_VERSION &&
    Array.isArray(current.credentials)
  ) {
    return {
      schemaVersion: STORE_SCHEMA_VERSION,
      credentials: sanitizeCredentials(current.credentials)
    };
  }

  // Migrate from legacy flat credentials key if present.
  const migrated: PersistedStoreV1 = {
    schemaVersion: STORE_SCHEMA_VERSION,
    credentials: sanitizeCredentials(loaded[CREDENTIALS_KEY])
  };
  await chrome.storage.local.set({ [STORE_KEY]: migrated });
  return migrated;
}

async function saveStore(store: PersistedStoreV1): Promise<void> {
  await chrome.storage.local.set({ [STORE_KEY]: store });
}

export async function getSettings(): Promise<Settings> {
  const loaded = await chrome.storage.local.get(SETTINGS_KEY);
  return {
    ...DEFAULT_SETTINGS,
    ...(loaded[SETTINGS_KEY] ?? {})
  } as Settings;
}

export async function saveSettings(settings: Settings): Promise<void> {
  await chrome.storage.local.set({ [SETTINGS_KEY]: settings });
}

export async function listCredentials(): Promise<PersistedCredential[]> {
  const store = await loadStore();
  return store.credentials;
}

export async function saveCredentials(records: PersistedCredential[]): Promise<void> {
  const store: PersistedStoreV1 = {
    schemaVersion: STORE_SCHEMA_VERSION,
    credentials: sanitizeCredentials(records)
  };
  await saveStore(store);
}

export async function upsertCredential(record: PersistedCredential): Promise<void> {
  const store = await loadStore();
  const index = store.credentials.findIndex((item) => item.credentialId === record.credentialId);
  if (index >= 0) {
    store.credentials[index] = record;
  } else {
    store.credentials.push(record);
  }
  await saveStore(store);
}
