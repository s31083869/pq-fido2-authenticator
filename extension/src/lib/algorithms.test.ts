// Extension 演算法支援清單與大小常數的測試（Day 6 T1）。
//
// 背景：決策 D3 規定 shared/pq-algorithms.json 是演算法資訊的唯一來源。Extension 的大小與 label
// 直接從共用表讀取；TypeScript 推不出 JSON 裡的字面值型別，所以 SupportedAlg 用的 as const 清單
// 仍寫在程式裡，由這裡比對共用表，兩者不一致就紅燈（Day 6「待你決定」第 1 點採 A）。
import { describe, expect, test } from "bun:test";
import { readFileSync } from "node:fs";

import * as signer from "@/background/pq-signer";
import {
  ALGORITHM_OPTIONS,
  PRIVATE_KEY_BYTES,
  PUBLIC_KEY_BYTES,
  SIGNATURE_BYTES,
  SUPPORTED_ALGORITHMS
} from "./algorithms";

// 共用演算法表，路徑相對於本測試檔：extension/src/lib → 專案根目錄/shared。
// 用檔案系統另外讀一次，不經過被測模組的 import，才能獨立比對。
const registry = JSON.parse(
  readFileSync(new URL("../../../shared/pq-algorithms.json", import.meta.url), "utf-8")
) as {
  algorithms: {
    label: string;
    coseAlg: number;
    publicKeyBytes: number;
    privateKeyBytes: number;
    signatureBytes: number;
  }[];
};

describe("extension algorithm registry", () => {
  // T1：支援清單依序等於共用表的 coseAlg，也等於決策 D1 定下的五個編號。
  // 依據：決策 D1、D3；workflow.md F07、F08。
  test("SUPPORTED_ALGORITHMS matches the shared registry in order", () => {
    // 放寬成 number[]，才能和 JSON 讀出來的 number 比較
    const supported: number[] = [...SUPPORTED_ALGORITHMS];
    expect(supported).toEqual(registry.algorithms.map((entry) => entry.coseAlg));
    expect(supported).toEqual([-48, -49, -50, -54, -55]);
  });

  // T1：三張大小表的每一筆都等於共用表（D3）。
  test("byte-size tables match the shared registry", () => {
    for (const entry of registry.algorithms) {
      const alg = entry.coseAlg as (typeof SUPPORTED_ALGORITHMS)[number];
      expect(PUBLIC_KEY_BYTES[alg]).toBe(entry.publicKeyBytes);
      expect(PRIVATE_KEY_BYTES[alg]).toBe(entry.privateKeyBytes);
      expect(SIGNATURE_BYTES[alg]).toBe(entry.signatureBytes);
    }
  });

  // T1：再用規格書的數值檢查一次，避免共用表本身被改錯時兩邊一起錯。
  // 依據：FIPS 204 Table 2（ML-DSA 公鑰／私鑰／簽章）；Falcon 第三輪規格 v1.2 第 3.11 節
  // （FN-DSA 公鑰／私鑰；簽章為不補滿格式的上限，見決策 D2）。
  test.each([
    ["ML-DSA-44", -48, 1312, 2560, 2420],
    ["ML-DSA-65", -49, 1952, 4032, 3309],
    ["ML-DSA-87", -50, 2592, 4896, 4627],
    ["FN-DSA-512", -54, 897, 1281, 752],
    ["FN-DSA-1024", -55, 1793, 2305, 1462]
  ] as const)("%s (%i) has the sizes from its specification", (_label, alg, pk, sk, sig) => {
    expect(PUBLIC_KEY_BYTES[alg]).toBe(pk);
    expect(PRIVATE_KEY_BYTES[alg]).toBe(sk);
    expect(SIGNATURE_BYTES[alg]).toBe(sig);
  });

  // T1：pq-signer.ts 對外提供的大小表必須就是這裡的表，不能另外寫死一份（workflow.md F10）。
  test("pq-signer re-exports the same tables", () => {
    expect(signer.PUBLIC_KEY_BYTES).toBe(PUBLIC_KEY_BYTES);
    expect(signer.PRIVATE_KEY_BYTES).toBe(PRIVATE_KEY_BYTES);
    expect(signer.SIGNATURE_BYTES).toBe(SIGNATURE_BYTES);
  });

  // T1：設定頁選單的資料來源（Day 6 第 3 項）。label 與 value 依序等於共用表的 label 與 coseAlg。
  test("ALGORITHM_OPTIONS matches the shared registry labels", () => {
    const options: { label: string; value: number }[] = ALGORITHM_OPTIONS.map(({ label, value }) => ({
      label,
      value
    }));
    expect(options).toEqual(
      registry.algorithms.map(({ label, coseAlg }) => ({ label, value: coseAlg }))
    );
  });
});
