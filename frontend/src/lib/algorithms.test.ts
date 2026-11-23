// 前端演算法選單與 pubKeyCredParams 重排規則的測試（Day 5 T4–T6）。
//
// 背景：前端是 RP 自己的網頁，它只能在 RP 發出的 pubKeyCredParams 清單「裡面」調整順序，
// 讓 demo 能指定優先測哪個演算法；不能替 RP 增加演算法（WebAuthn §5.4：清單內容由 RP 決定，
// 順序代表 RP 的偏好）。authenticator 會挑清單中第一個自己支援的（WebAuthn §6.3.2）。
import { describe, expect, test } from "bun:test";
import { readFileSync } from "node:fs";

import { ALGORITHM_OPTIONS, orderPubKeyCredParams, type PubKeyCredParam } from "./algorithms";

// 共用演算法表（決策 D3 的唯一資料來源），路徑相對於本測試檔：frontend/src/lib → 專案根目錄/shared
const registry = JSON.parse(
  readFileSync(new URL("../../../shared/pq-algorithms.json", import.meta.url), "utf-8"),
) as { algorithms: { label: string; coseAlg: number }[] };

// 把 COSE 編號清單包成 pubKeyCredParams 的格式：每一筆都是 {type: "public-key", alg}
const params = (algs: number[]): PubKeyCredParam[] =>
  algs.map((alg) => ({ type: "public-key", alg }));

// RP 預設的 hosted_algorithms（rp_server/config.py，D6）：ML-DSA-65、ML-DSA-44、ML-DSA-87、FN-DSA-512、FN-DSA-1024
const RP_DEFAULT = [-49, -48, -50, -54, -55];

describe("ALGORITHM_OPTIONS", () => {
  // T4：選單必須和共用表一致（D3：其他層用測試檢查一致）。依據 workflow.md F01。
  test("matches the shared algorithm registry in order", () => {
    expect(ALGORITHM_OPTIONS).toHaveLength(5);
    expect(ALGORITHM_OPTIONS.map(({ label, value }) => ({ label, value }))).toEqual(
      registry.algorithms.map(({ label, coseAlg }) => ({ label, value: coseAlg })),
    );
  });
});

describe("orderPubKeyCredParams", () => {
  // T5：選到的演算法在 RP 的清單裡 → 移到第一個，其他保持原本的相對順序，不新增也不刪除。
  // 依據 FN-DSA-PLAN.md Day 5「排序只在 RP 有宣告的演算法中進行」；WebAuthn §5.4。
  test.each([
    ["a FN-DSA-512", -54, [-54, -49, -48, -50, -55]],
    ["b FN-DSA-1024", -55, [-55, -49, -48, -50, -54]],
    ["c ML-DSA-65 (already first)", -49, [-49, -48, -50, -54, -55]],
    ["d ML-DSA-87", -50, [-50, -49, -48, -54, -55]],
  ])("moves the preferred algorithm to the front: %s", (_name, preferred, expected) => {
    const ordered = orderPubKeyCredParams(params(RP_DEFAULT), preferred);

    expect(ordered.map((param) => param.alg)).toEqual(expected);
    // 每一筆的 type 都維持 public-key（WebAuthn §5.3 PublicKeyCredentialParameters）
    expect(ordered.every((param) => param.type === "public-key")).toBe(true);
    // 項目集合和 RP 發出的完全相同：沒有新增，也沒有刪除
    expect([...ordered.map((param) => param.alg)].sort()).toEqual([...RP_DEFAULT].sort());
  });

  // T6：選到的演算法 RP 沒宣告 → 拋出錯誤、不回傳任何清單，前端因此不會呼叫
  // navigator.credentials.create，也不會跳出 Windows Hello（Day 5「待你決定」第 1 點採 A）。
  // 錯誤訊息必須同時指出「RP 沒有宣告」與演算法名稱，只含名稱的其他錯誤不算（依獨立審查加嚴）。
  // 依據 workflow.md F16；WebAuthn §5.4（前端不能替 RP 增加演算法）。
  test("throws when the RP does not offer the preferred algorithm", () => {
    expect(() => orderPubKeyCredParams(params([-49, -48, -50]), -54)).toThrow(
      /does not offer FN-DSA-512/,
    );
  });
});
