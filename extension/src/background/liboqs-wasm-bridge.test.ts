// 真的 pq_bridge.wasm 的測試（Day 7 T1–T4）。
//
// 背景：Extension 的其他測試都用假的簽章器，碰不到 WASM。這裡直接讀進 git 的
// extension/public/wasm/pq_bridge.wasm，呼叫裡面真的 liboqs，確認 C 端的 COSE → liboqs 對應（pq_bridge.c）
// 與編譯清單（setup-liboqs-emscripten.sh）都正確。重建 WASM 前後各跑一次：ML-DSA 前後都要綠燈，
// 才能說加入 Falcon 沒有改變 ML-DSA 的行為。
import { beforeAll, describe, expect, test } from "bun:test";
import { readFileSync } from "node:fs";

import type { SupportedAlg } from "@/types/messages";
import { LiboqsWasmBridge } from "./liboqs-wasm-bridge";

// 進 git 的 WASM 檔，路徑相對於本測試檔：extension/src/background → extension/public/wasm
const WASM_BYTES = readFileSync(new URL("../../public/wasm/pq_bridge.wasm", import.meta.url));

// 各演算法的公鑰／私鑰／簽章大小（bytes），取自規格書，不取自被測程式：
// ML-DSA：FIPS 204 Table 2；FN-DSA：Falcon 第三輪規格 v1.2 第 3.11 節（簽章為不補滿格式的上限，決策 D2）。
const SPEC_SIZES = [
  ["ML-DSA-44", -48, 1312, 2560, 2420],
  ["ML-DSA-65", -49, 1952, 4032, 3309],
  ["ML-DSA-87", -50, 2592, 4896, 4627],
  ["FN-DSA-512", -54, 897, 1281, 752],
  ["FN-DSA-1024", -55, 1793, 2305, 1462]
] as const;

// 簽章用的固定訊息：內容不重要，只要每次相同
const MESSAGE = new TextEncoder().encode("Day 7 WASM bridge test message");

let bridge: LiboqsWasmBridge;

beforeAll(async () => {
  bridge = await LiboqsWasmBridge.fromBytes(WASM_BYTES);
});

describe("pq_bridge.wasm", () => {
  // T1：WASM 回報的大小等於規格書（也就是共用演算法表）。FN-DSA-512 的簽章大小必須是 752，
  // 不是補滿格式 Falcon-padded-512 的 666：兩種格式的金鑰大小相同，只有這裡分得出 C 端選了哪一種。
  // 依據：決策 D2、D3（C bridge 以測試檢查與共用表一致）；FIPS 204 Table 2；Falcon v1.2 第 3.11 節；workflow.md F12。
  test.each(SPEC_SIZES)("T1 %s (%i) reports the specified sizes", (_label, alg, pk, sk, sig) => {
    expect(bridge.publicKeyBytes(alg)).toBe(pk);
    expect(bridge.secretKeyBytes(alg)).toBe(sk);
    expect(bridge.signatureBytes(alg)).toBe(sig);
  });

  // T2：產生的金鑰長度正確，而且兩次結果不同（random_get 有接上真的亂數）。
  // 依據：workflow.md F11、F12；FIPS 204 與 Falcon v1.2 的金鑰產生都使用隨機性。
  test.each(SPEC_SIZES)("T2 %s (%i) generates fresh keys of the specified sizes", (_label, alg, pk, sk) => {
    const first = bridge.generateKeyPair(alg);
    const second = bridge.generateKeyPair(alg);

    expect(first.publicKey).toHaveLength(pk);
    expect(first.privateKey).toHaveLength(sk);
    expect(second.publicKey).toHaveLength(pk);
    expect([...first.publicKey]).not.toEqual([...second.publicKey]);
  });

  // T3 (a)：ML-DSA 的簽章長度固定，剛好等於規格值。依據：FIPS 204 Table 2。
  test.each(SPEC_SIZES.slice(0, 3))("T3a %s (%i) signs with the fixed length", (_label, alg, _pk, _sk, sig) => {
    const { privateKey } = bridge.generateKeyPair(alg);
    expect(bridge.sign(alg, privateKey, MESSAGE)).toHaveLength(sig);
  });

  // T3 (b)：FN-DSA 不補滿格式。同一把私鑰對同一則訊息簽 20 次（每次 nonce 不同）：
  // 每個長度都不超過上限、20 個長度不全相同、第一個 byte 是標頭 0x30 + logn（512：logn = 9；1024：logn = 10）。
  // 依據：Falcon v1.2 第 3.11.3 節（標頭）、第 3.11.6 節（長度不固定）；workflow.md F10。
  test.each([
    ["FN-DSA-512", -54, 752, 0x39],
    ["FN-DSA-1024", -55, 1462, 0x3a]
  ] as const)("T3b %s (%i) signs in the unpadded compressed format", (_label, alg, maxLength, header) => {
    const { privateKey } = bridge.generateKeyPair(alg);
    const signatures = Array.from({ length: 20 }, () => bridge.sign(alg, privateKey, MESSAGE));

    for (const signature of signatures) {
      expect(signature.length).toBeLessThanOrEqual(maxLength);
      expect(signature[0]).toBe(header);
    }
    expect(new Set(signatures.map((signature) => signature.length)).size).toBeGreaterThan(1);
  });

  // T4：只對應 -54/-55，沒有誤加鄰近編號或 ES256。C 端回 -1，bridge 丟錯。
  // 依據：決策 D1；workflow.md F11。
  test.each([-7, -53, -56])("T4 rejects unsupported COSE alg %i", (alg) => {
    const unsupported = alg as unknown as SupportedAlg;
    expect(() => bridge.publicKeyBytes(unsupported)).toThrow();
    expect(() => bridge.secretKeyBytes(unsupported)).toThrow();
    expect(() => bridge.signatureBytes(unsupported)).toThrow();
    expect(() => bridge.generateKeyPair(unsupported)).toThrow();
  });
});
