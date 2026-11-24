import { beforeEach, describe, expect, test } from "bun:test";
import { base64UrlToBytes } from "@/lib/base64url";
import { PQAuthenticator, WebAuthnError } from "./authenticator";
import type {
  CreationRequestPayload,
  RequestRequestPayload,
  Settings,
  SupportedAlg
} from "@/types/messages";
import {
  PRIVATE_KEY_BYTES,
  PUBLIC_KEY_BYTES,
  SIGNATURE_BYTES,
  type GeneratedKeyPair,
  type PQSigner
} from "./pq-signer";
import { listCredentials } from "./store";
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

/**
 * FN-DSA 假簽章的長度（bytes），刻意比上限（SIGNATURE_BYTES：752／1462）短。
 *
 * 為什麼：Falcon 不補滿格式的簽章長度不固定（Falcon v1.2 第 3.11.6 節），authenticator 必須原封不動
 * 回傳。若假簽章剛好等於上限，「補零到上限」的錯誤實作也會產生相同長度，測試分不出來（Day 6 T4）。
 */
const FN_DSA_TEST_SIGNATURE_BYTES: Partial<Record<SupportedAlg, number>> = {
  [-54]: 650,
  [-55]: 1300
};

/**
 * 測試用的假簽章器：不做真的密碼學，只產生固定長度、可重現的 bytes，並記錄被呼叫的情形。
 *
 * 為什麼用假的：Day 6 的 WASM 還沒有 Falcon（Day 7 才加入），bun 測試也不載入 WASM。
 * 真的「產生金鑰 → 簽章 → RP 驗章」由 Python 端的測試與 Day 7 之後的 WASM 測試負責（CLAUDE.md「真實密碼學」）。
 * 金鑰長度取自共用表；簽章長度 ML-DSA 用固定長度，FN-DSA 用 FN_DSA_TEST_SIGNATURE_BYTES。
 */
class TestSigner implements PQSigner {
  private counter = 0;
  /** generateKeyPair 每次被呼叫時收到的演算法，依呼叫順序排列 */
  readonly keygenCalls: SupportedAlg[] = [];
  /** sign 每次被呼叫時收到的演算法與私鑰長度，依呼叫順序排列 */
  readonly signCalls: Array<{ algorithm: SupportedAlg; privateKeyLength: number }> = [];
  /** 最近一次 sign 回傳的簽章，用來確認 authenticator 原封不動放進回應 */
  lastSignature: Uint8Array | null = null;

  /**
   * 產生假的金鑰對，並把收到的演算法記進 keygenCalls（T2、T5 用來確認選了哪個演算法、或完全沒有產生金鑰）。
   *
   * @param algorithm authenticator 選到的 COSE 演算法編號
   * @returns 長度等於共用表 publicKeyBytes／privateKeyBytes 的可重現 bytes；每次呼叫內容都不同
   */
  async generateKeyPair(algorithm: SupportedAlg): Promise<GeneratedKeyPair> {
    this.keygenCalls.push(algorithm);
    const run = this.counter++;
    return {
      publicKey: deterministicBytes(`pk-${algorithm}-${run}`, PUBLIC_KEY_BYTES[algorithm]),
      privateKey: deterministicBytes(`sk-${algorithm}-${run}`, PRIVATE_KEY_BYTES[algorithm])
    };
  }

  /**
   * 產生假的簽章，並把演算法與私鑰長度記進 signCalls、把回傳值存進 lastSignature（T4 用來比對）。
   *
   * 長度：FN-DSA 用 FN_DSA_TEST_SIGNATURE_BYTES（650／1300，刻意比上限短）；ML-DSA 用固定長度 SIGNATURE_BYTES。
   *
   * @param algorithm 憑證的 COSE 演算法編號
   * @param privateKey 從 chrome.storage 取回的私鑰
   * @param message 要簽的資料（authData ‖ SHA-256(clientDataJSON)，WebAuthn §6.3.3）
   * @returns 由演算法、私鑰與訊息決定的可重現 bytes
   */
  async sign(algorithm: SupportedAlg, privateKey: Uint8Array, message: Uint8Array): Promise<Uint8Array> {
    this.signCalls.push({ algorithm, privateKeyLength: privateKey.length });
    // 指紋包含私鑰與訊息，所以不同的 authData（signCount 不同）會得到不同的假簽章
    const fingerprint = `${algorithm}-${hashHex(privateKey)}-${hashHex(message)}`;
    const length = FN_DSA_TEST_SIGNATURE_BYTES[algorithm] ?? SIGNATURE_BYTES[algorithm];
    this.lastSignature = deterministicBytes(`sig-${algorithm}-${fingerprint}`, length);
    return this.lastSignature;
  }
}

/**
 * 從 authenticatorData 取出 credentialPublicKey（CBOR 編碼的 COSE_Key）。
 *
 * authData 的位置（WebAuthn §6.1 與 Attested Credential Data 一節）：rpIdHash 32 + flags 1 + signCount 4
 * + AAGUID 16 + credentialId 長度 2（大端序）+ credentialId，之後就是 COSE_Key。
 * 註冊時 flags 沒有 ED（extensions），所以 COSE_Key 一路到 authData 結尾。
 *
 * @param authenticatorDataB64 回應中的 authenticatorData（base64url）
 * @returns COSE_Key 的 bytes
 */
function extractCredentialPublicKey(authenticatorDataB64: string): Uint8Array {
  const bytes = base64UrlToBytes(authenticatorDataB64);
  const credentialIdLengthOffset = 32 + 1 + 4 + 16;
  const credentialIdLength = (bytes[credentialIdLengthOffset] << 8) | bytes[credentialIdLengthOffset + 1];
  return bytes.slice(credentialIdLengthOffset + 2 + credentialIdLength);
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

  // T2：依 RP 清單的順序，選第一個 Extension 支援的演算法；回應、簽章器、storage 三處一致。
  // 依據：workflow.md F08（[-7, -54] 選 -54）、F13、F14（storage 保存 algorithm）；WebAuthn §6.3.2（Level 2 第 7 步：用清單中第一個支援的演算法產生金鑰）。
  test.each([
    ["a ES256 then FN-DSA-512", [-7, -54], -54],
    ["b FN-DSA-1024 only", [-55], -55],
    ["c FN-DSA-1024 before FN-DSA-512", [-7, -55, -54], -55],
    ["d ML-DSA-65 before FN-DSA-512", [-49, -54], -49]
  ] as const)("create follows the RP order with FN-DSA: %s", async (_name, offered, expected) => {
    const signer = new TestSigner();
    const authenticator = new PQAuthenticator(signer);
    const result = await authenticator.makeCredential(makeCreatePayload([...offered]), SETTINGS);

    expect(result.response.publicKeyAlgorithm).toBe(expected);
    expect(signer.keygenCalls).toEqual([expected]);
    const stored = await listCredentials();
    expect(stored).toHaveLength(1);
    expect(stored[0].algorithm).toBe(expected);
  });

  // T3：COSE_Key {1: 7, 3: alg, -1: 公鑰} 的 CBOR bytes。預期的 10 bytes 依 RFC 8949 第 3.1 節手算，
  // 不用 Extension 自己的 encodeCbor() 產生，避免拿被測的編碼器驗證它自己（CLAUDE.md「避免球員兼裁判」）：
  //   A3 = 3 組鍵值的 map；01 07 = kty 7（AKP，RFC 9964）；03 = alg 鍵；
  //   38 35 = -54（major type 1，值 53）／38 36 = -55（值 54）；20 = 鍵 -1；
  //   59 03 81 = 897 bytes 的 byte string／59 07 01 = 1793 bytes。
  // 依據：workflow.md F09；RFC 9964；RFC 8949 第 3.1 節；WebAuthn §6.1。
  test.each([
    ["FN-DSA-512", -54, [0xa3, 0x01, 0x07, 0x03, 0x38, 0x35, 0x20, 0x59, 0x03, 0x81], 897],
    ["FN-DSA-1024", -55, [0xa3, 0x01, 0x07, 0x03, 0x38, 0x36, 0x20, 0x59, 0x07, 0x01], 1793]
  ] as const)("create encodes the %s COSE_Key", async (_name, alg, header, publicKeyLength) => {
    const authenticator = new PQAuthenticator(new TestSigner());
    const result = await authenticator.makeCredential(makeCreatePayload([alg]), SETTINGS);

    const coseKey = extractCredentialPublicKey(result.response.authenticatorData);
    expect([...coseKey.slice(0, header.length)]).toEqual([...header]);
    // 標頭之後就是公鑰本身，必須等於回應中的 publicKey，而且之後沒有其他資料
    const publicKey = coseKey.slice(header.length);
    expect(publicKey).toHaveLength(publicKeyLength);
    expect([...publicKey]).toEqual([...base64UrlToBytes(result.response.publicKey)]);
  });

  // T4：FN-DSA 登入。簽章器收到正確的演算法與私鑰；回應的簽章與簽章器回傳的完全相同，
  // 長度不固定、不補到上限（假簽章故意比上限短，見 FN_DSA_TEST_SIGNATURE_BYTES）。
  // 依據：workflow.md F10、F15；Falcon v1.2 第 3.11.6 節；共用表 signatureLengthFixed: false；WebAuthn §6.1.1。
  test.each([
    ["FN-DSA-512", -54, 1281, 650],
    ["FN-DSA-1024", -55, 2305, 1300]
  ] as const)("assertion returns the %s signature unchanged", async (_name, alg, privateKeyLength, signatureLength) => {
    const signer = new TestSigner();
    const authenticator = new PQAuthenticator(signer);
    const created = await authenticator.makeCredential(makeCreatePayload([alg]), SETTINGS);
    const assertion = await authenticator.getAssertion(makeGetPayload(created.id), SETTINGS);

    expect(signer.signCalls).toEqual([{ algorithm: alg, privateKeyLength }]);
    const signature = base64UrlToBytes(assertion.response.signature);
    expect(signature).toHaveLength(signatureLength);
    expect(signature).toEqual(signer.lastSignature as Uint8Array);
    expect(parseSignCount(assertion.response.authenticatorData)).toBe(1);
  });

  // T5：設定的 defaultAlgorithm 為 FN-DSA-512，也不能讓 Extension 選 RP 沒宣告的演算法。
  // 依據：workflow.md F16；WebAuthn §6.3.2 第 2 步（都不支援時回 NotSupportedError）。
  describe("with defaultAlgorithm set to FN-DSA-512", () => {
    const fnDsaDefault: Settings = { ...SETTINGS, defaultAlgorithm: -54 };

    // (a) RP 沒宣告 FN-DSA → 選 RP 清單中第一個支援的 ML-DSA-65
    test("create picks the RP's ML-DSA instead of the default", async () => {
      const signer = new TestSigner();
      const authenticator = new PQAuthenticator(signer);
      const result = await authenticator.makeCredential(makeCreatePayload([-49, -48, -50]), fnDsaDefault);

      expect(result.response.publicKeyAlgorithm).toBe(-49);
      expect(signer.keygenCalls).toEqual([-49]);
    });

    // (b) RP 沒有任何 PQ 演算法 → NotSupportedError，不產生金鑰、不存任何憑證
    test("create rejects without generating a key when nothing is supported", async () => {
      const signer = new TestSigner();
      const authenticator = new PQAuthenticator(signer);

      let caught: unknown;
      try {
        await authenticator.makeCredential(makeCreatePayload([-7, -257]), fnDsaDefault);
      } catch (error) {
        caught = error;
      }
      expect(caught).toBeInstanceOf(WebAuthnError);
      expect((caught as WebAuthnError).name).toBe("NotSupportedError");
      expect(signer.keygenCalls).toEqual([]);
      expect(await listCredentials()).toEqual([]);
    });
  });
});
