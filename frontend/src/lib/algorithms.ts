// 前端的演算法選單與 pubKeyCredParams 重排規則。
//
// 誰決定什麼（WebAuthn §5.4、§6.3.2、§7.1）：
// - RP 用 hosted_algorithms 決定接受哪些演算法與偏好順序，發出 pubKeyCredParams；
// - 前端（RP 自己的網頁）只能在這份清單「裡面」調整順序，讓 demo 能指定優先嘗試的演算法；
// - authenticator 依清單順序，選第一個自己支援的；RP 最後再檢查回來的 alg 是否宣告過。
// 選單上選的是「優先嘗試」，authenticator 不支援時會改選清單中下一個（Day 5 待辦：顯示實際選到的演算法）。

/** pubKeyCredParams 的一筆：type 固定為 public-key，alg 是 COSE 演算法編號（WebAuthn §5.3）。 */
export type PubKeyCredParam = { type: "public-key"; alg: number };

/**
 * 註冊頁的演算法選單：label 給使用者看，value 是 COSE 演算法編號。
 *
 * 內容與順序必須和共用演算法表 shared/pq-algorithms.json 相同（決策 D3），
 * 由 algorithms.test.ts 的 T4 比對；前端不直接 import 那份 JSON，避免修改 Next.js 的建置設定
 * （Day 5「待你決定」第 2 點）。FN-DSA 的 -54/-55 是 draft-ietf-cose-falcon 的暫定編號。
 */
export const ALGORITHM_OPTIONS: readonly { label: string; value: number }[] = [
  { label: "ML-DSA-44", value: -48 },
  { label: "ML-DSA-65", value: -49 },
  { label: "ML-DSA-87", value: -50 },
  { label: "FN-DSA-512", value: -54 },
  { label: "FN-DSA-1024", value: -55 },
];

/**
 * 把使用者選的演算法移到 RP 清單的第一個，其他項目保持原本的相對順序。
 *
 * 為什麼：authenticator 會選清單中第一個自己支援的（WebAuthn §6.3.2），所以排到第一個就是「優先嘗試」。
 * 前端不能替 RP 增加演算法：RP 沒宣告的演算法即使送出，RP 的 /register/verify 也會回 400，
 * 而且使用者會先白白完成一次 Windows Hello。因此 RP 沒宣告時直接拋出錯誤，讓呼叫端在
 * navigator.credentials.create 之前停下（Day 5「待你決定」第 1 點採 A）。
 *
 * @param rpParams RP 在 /register/options 發出的 pubKeyCredParams（依 RP 偏好排序）
 * @param preferredAlg 選單上選的 COSE 演算法編號
 * @returns 重排後的新清單；項目與 rpParams 完全相同，只有順序不同；不修改 rpParams
 * @throws Error RP 的清單裡沒有 preferredAlg 時，訊息包含該演算法的名稱
 */
export function orderPubKeyCredParams(
  rpParams: readonly PubKeyCredParam[],
  preferredAlg: number,
): PubKeyCredParam[] {
  const preferred = rpParams.filter((param) => param.alg === preferredAlg);
  if (preferred.length === 0) {
    const label =
      ALGORITHM_OPTIONS.find((option) => option.value === preferredAlg)?.label ??
      `COSE ${preferredAlg}`;
    throw new Error(`The RP does not offer ${label} (${preferredAlg})`);
  }
  return [...preferred, ...rpParams.filter((param) => param.alg !== preferredAlg)];
}
