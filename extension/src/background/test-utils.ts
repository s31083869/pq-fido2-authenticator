import { bytesToBase64Url } from "@/lib/base64url";

function fnv1a(seed: number, bytes: Uint8Array): number {
  let hash = seed >>> 0;
  for (const value of bytes) {
    hash ^= value;
    hash = Math.imul(hash, 0x01000193) >>> 0;
  }
  return hash >>> 0;
}

function xorshift32(state: number): number {
  let x = state >>> 0;
  x ^= x << 13;
  x ^= x >>> 17;
  x ^= x << 5;
  return x >>> 0;
}

export function deterministicBytes(seed: string, length: number): Uint8Array {
  const seedBytes = new TextEncoder().encode(seed);
  let state = fnv1a(0x811c9dc5, seedBytes);
  const out = new Uint8Array(length);
  for (let i = 0; i < length; i += 1) {
    state = xorshift32(state);
    out[i] = state & 0xff;
  }
  return out;
}

export function deterministicBase64Url(seed: string, length: number): string {
  return bytesToBase64Url(deterministicBytes(seed, length));
}

export function createChromeStorageMock(seed: Record<string, unknown> = {}) {
  const db: Record<string, unknown> = { ...seed };
  return {
    storage: {
      local: {
        async get(keys?: string | string[] | Record<string, unknown>) {
          if (typeof keys === "string") {
            return { [keys]: db[keys] };
          }
          if (Array.isArray(keys)) {
            return keys.reduce<Record<string, unknown>>((acc, key) => {
              acc[key] = db[key];
              return acc;
            }, {});
          }
          if (keys && typeof keys === "object") {
            return Object.keys(keys).reduce<Record<string, unknown>>((acc, key) => {
              acc[key] = db[key] ?? (keys as Record<string, unknown>)[key];
              return acc;
            }, {});
          }
          return { ...db };
        },
        async set(items: Record<string, unknown>) {
          Object.assign(db, items);
        }
      }
    },
    __db: db
  };
}
