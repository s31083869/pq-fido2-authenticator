import { beforeEach, describe, expect, test } from "bun:test";
import { base64UrlToBytes } from "@/lib/base64url";
import { PQAuthenticator, WebAuthnError } from "./authenticator";
import type { CreationRequestPayload, RequestRequestPayload, Settings } from "@/types/messages";
import {
  PRIVATE_KEY_BYTES,
  PUBLIC_KEY_BYTES,
  SIGNATURE_BYTES,
  type GeneratedKeyPair,
  type PQSigner
} from "./pq-signer";
import { createChromeStorageMock, deterministicBase64Url, deterministicBytes } from "./test-utils";

const SETTINGS: Settings = {
  enabled: true,
  defaultAlgorithm: -48,
  uvMode: "soft-auto"
};

function hashHex(bytes: Uint8Array): string {
  let hash = 0x811c9dc5;
  for (const value of bytes) {
    hash ^= value;
    hash = Math.imul(hash, 0x01000193) >>> 0;
  }
  return hash.toString(16).padStart(8, "0");
}

class TestSigner implements PQSigner {
  private counter = 0;

  async generateKeyPair(algorithm: -48 | -49 | -50): Promise<GeneratedKeyPair> {
    const run = this.counter++;
    return {
      publicKey: deterministicBytes(`pk-${algorithm}-${run}`, PUBLIC_KEY_BYTES[algorithm]),
      privateKey: deterministicBytes(`sk-${algorithm}-${run}`, PRIVATE_KEY_BYTES[algorithm])
    };
  }

  async sign(
    algorithm: -48 | -49 | -50,
    privateKey: Uint8Array,
    message: Uint8Array
  ): Promise<Uint8Array> {
    const fingerprint = `${algorithm}-${hashHex(privateKey)}-${hashHex(message)}`;
    return deterministicBytes(`sig-${algorithm}-${fingerprint}`, SIGNATURE_BYTES[algorithm]);
  }
}

function parseSignCount(authenticatorDataB64: string): number {
  const bytes = base64UrlToBytes(authenticatorDataB64);
  const offset = 33;
  return (
    (bytes[offset] << 24) |
    (bytes[offset + 1] << 16) |
    (bytes[offset + 2] << 8) |
    bytes[offset + 3]
  );
}

function parseFlags(authenticatorDataB64: string): number {
  const bytes = base64UrlToBytes(authenticatorDataB64);
  return bytes[32];
}

function parseClientData(clientDataB64: string): Record<string, unknown> {
  const bytes = base64UrlToBytes(clientDataB64);
  return JSON.parse(new TextDecoder().decode(bytes)) as Record<string, unknown>;
}

function makeCreatePayload(params: number[] = [-48, -49, -50]): CreationRequestPayload {
  return {
    origin: "https://demo.yubico.com",
    publicKey: {
      rp: {
        id: "demo.yubico.com",
        name: "Yubico Demo"
      },
      user: {
        id: deterministicBase64Url("test-user-id", 32),
        name: "tester",
        displayName: "tester"
      },
      challenge: deterministicBase64Url("create-challenge", 32),
      pubKeyCredParams: params.map((alg) => ({ type: "public-key", alg })),
      excludeCredentials: [],
      extensions: {
        credProps: true
      },
      timeout: 90_000,
      attestation: "direct"
    }
  };
}

function makeGetPayload(credentialId?: string): RequestRequestPayload {
  return {
    origin: "https://demo.yubico.com",
    publicKey: {
      challenge: deterministicBase64Url("get-challenge", 32),
      rpId: "demo.yubico.com",
      allowCredentials: credentialId
        ? [{ type: "public-key", id: credentialId }]
        : undefined
    }
  };
}

describe("PQAuthenticator", () => {
  beforeEach(() => {
    (globalThis as unknown as { chrome: unknown }).chrome = createChromeStorageMock();
  });

  test("create selects first supported algorithm from request order", async () => {
    const authenticator = new PQAuthenticator(new TestSigner());
    const result = await authenticator.makeCredential(makeCreatePayload([-7, -49, -48]), SETTINGS);
    expect(result.response.publicKeyAlgorithm).toBe(-49);
  });

  test("create returns AT+UP+UV flags and signCount=0", async () => {
    const authenticator = new PQAuthenticator(new TestSigner());
    const result = await authenticator.makeCredential(makeCreatePayload(), SETTINGS);

    expect(parseFlags(result.response.authenticatorData)).toBe(0x45);
    expect(parseSignCount(result.response.authenticatorData)).toBe(0);
    expect(result.response.transports).toEqual(["internal"]);
    expect(result.clientExtensionResults).toEqual({ credProps: { rk: false } });
    expect(parseClientData(result.response.clientDataJSON).crossOrigin).toBe(false);
  });

  test("create throws NotSupportedError when no PQ algorithm is offered", async () => {
    const authenticator = new PQAuthenticator(new TestSigner());
    await expect(authenticator.makeCredential(makeCreatePayload([-7, -8]), SETTINGS)).rejects.toBeInstanceOf(
      WebAuthnError
    );

    try {
      await authenticator.makeCredential(makeCreatePayload([-7, -8]), SETTINGS);
    } catch (error) {
      expect((error as WebAuthnError).name).toBe("NotSupportedError");
    }
  });

  test("assertion increments signCount monotonically", async () => {
    const authenticator = new PQAuthenticator(new TestSigner());
    const created = await authenticator.makeCredential(makeCreatePayload(), SETTINGS);

    const first = await authenticator.getAssertion(makeGetPayload(created.id), SETTINGS);
    const second = await authenticator.getAssertion(makeGetPayload(created.id), SETTINGS);

    expect(parseFlags(first.response.authenticatorData)).toBe(0x05);
    expect(parseSignCount(first.response.authenticatorData)).toBe(1);
    expect(parseSignCount(second.response.authenticatorData)).toBe(2);
    expect(base64UrlToBytes(first.response.signature)).toHaveLength(SIGNATURE_BYTES[-48]);
    expect(base64UrlToBytes(second.response.signature)).toHaveLength(SIGNATURE_BYTES[-48]);
    expect(first.response.signature).not.toBe(second.response.signature);
  });

  test("create rejects rpId/origin mismatch", async () => {
    const authenticator = new PQAuthenticator(new TestSigner());
    const payload = makeCreatePayload();
    payload.publicKey.rp.id = "example.com";

    try {
      await authenticator.makeCredential(payload, SETTINGS);
      throw new Error("expected makeCredential to throw");
    } catch (error) {
      expect((error as WebAuthnError).name).toBe("SecurityError");
    }
  });

  test("get rejects rpId/origin mismatch", async () => {
    const authenticator = new PQAuthenticator(new TestSigner());
    const created = await authenticator.makeCredential(makeCreatePayload(), SETTINGS);

    const payload = makeGetPayload(created.id);
    payload.publicKey.rpId = "example.com";

    try {
      await authenticator.getAssertion(payload, SETTINGS);
      throw new Error("expected getAssertion to throw");
    } catch (error) {
      expect((error as WebAuthnError).name).toBe("SecurityError");
    }
  });

  test("create aborts when native-touch-id UV host is unavailable", async () => {
    const authenticator = new PQAuthenticator(new TestSigner());
    const nativeUvSettings: Settings = {
      ...SETTINGS,
      uvMode: "native-touch-id"
    };

    try {
      await authenticator.makeCredential(makeCreatePayload(), nativeUvSettings);
      throw new Error("expected makeCredential to throw");
    } catch (error) {
      expect((error as WebAuthnError).name).toBe("NotAllowedError");
    }
  });
});
