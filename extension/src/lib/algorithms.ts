// Extension 支援的後量子簽章演算法，以及各演算法的金鑰／簽章大小。
//
// 資料來源：決策 D3 的共用演算法表 shared/pq-algorithms.json，RP、Python authenticator、
// 前端與 Extension 都以它為準。大小與 label 直接從共用表讀取；COSE 編號另外寫一份 as const 清單，
// 因為 TypeScript 無法從 JSON 推出 -48 | -49 | … 這種字面值型別，一致性由 algorithms.test.ts 的 T1 檢查。
// FN-DSA 的 -54/-55 是 draft-ietf-cose-falcon 申請中的暫定編號（決策 D1，共用表 status 為 provisional）。
import registry from "../../../shared/pq-algorithms.json";

/**
 * Extension 支援的 COSE 演算法編號，順序與共用表相同。
 *
 * -48/-49/-50 為 ML-DSA-44/65/87（RFC 9964、FIPS 204）；-54/-55 為 FN-DSA-512/1024
 * （Falcon 第三輪規格 v1.2，透過 liboqs 的 Falcon-512/1024 實作，決策 D2）。
 * authenticator 只從 RP 的 pubKeyCredParams 中挑選這些編號（WebAuthn §6.3.2 第 2 步與 Level 2 第 7 步）。
 */
export const SUPPORTED_ALGORITHMS = [-48, -49, -50, -54, -55] as const;

/** Extension 支援的 COSE 演算法編號型別，由 SUPPORTED_ALGORITHMS 推出。 */
export type SupportedAlg = (typeof SUPPORTED_ALGORITHMS)[number];

/** 共用演算法表中單一演算法的欄位（欄位意義見 shared/pq-algorithms.json 的 description）。 */
type RegistryEntry = (typeof registry.algorithms)[number];

/**
 * 判斷 RP 送來的 COSE 編號是否為 Extension 支援的演算法。
 *
 * @param alg pubKeyCredParams 裡的 alg（任意整數，可能是 -7 ES256 這類非 PQ 演算法）
 * @returns 支援時回傳 true，同時讓 TypeScript 把 alg 收窄成 SupportedAlg
 */
export function isSupportedAlg(alg: number): alg is SupportedAlg {
  return (SUPPORTED_ALGORITHMS as readonly number[]).includes(alg);
}

/**
 * 從共用表取出某個演算法的那一筆。
 *
 * 找不到就在模組載入時直接丟出錯誤：代表 SUPPORTED_ALGORITHMS 與共用表不一致，
 * 繼續執行只會在簽章時才以難懂的方式失敗。
 *
 * @param alg 支援清單中的 COSE 編號
 * @returns 共用表中 coseAlg 等於 alg 的那一筆
 */
function registryEntry(alg: SupportedAlg): RegistryEntry {
  const entry = registry.algorithms.find((candidate) => candidate.coseAlg === alg);
  if (!entry) {
    throw new Error(`shared/pq-algorithms.json has no entry for COSE alg ${alg}`);
  }
  return entry;
}

/**
 * 依支援清單建立「COSE 編號 → 大小」的對照表。
 *
 * @param field 要取的共用表欄位（publicKeyBytes、privateKeyBytes 或 signatureBytes）
 * @returns 每個支援的演算法各一筆的對照表，單位為 bytes
 */
function sizeTable(
  field: "publicKeyBytes" | "privateKeyBytes" | "signatureBytes"
): Readonly<Record<SupportedAlg, number>> {
  const table = {} as Record<SupportedAlg, number>;
  for (const alg of SUPPORTED_ALGORITHMS) {
    table[alg] = registryEntry(alg)[field];
  }
  return Object.freeze(table);
}

/** 公鑰大小（bytes），也就是 COSE_Key 中 -1（pub）欄位的長度。 */
export const PUBLIC_KEY_BYTES = sizeTable("publicKeyBytes");

/** 私鑰大小（bytes），存在 chrome.storage 的 privateKey 解碼後應為此長度。 */
export const PRIVATE_KEY_BYTES = sizeTable("privateKeyBytes");

/**
 * 簽章大小（bytes）。
 *
 * ML-DSA 的簽章長度固定，這裡就是實際長度。FN-DSA 採不補滿格式（Falcon v1.2 第 3.11.6 節），
 * 每次簽章長度不同，這裡是上限（共用表 signatureLengthFixed 為 false）：只能用來配置緩衝區，
 * 不可以把簽章補到這個長度，也不可以要求簽章剛好這麼長。
 */
export const SIGNATURE_BYTES = sizeTable("signatureBytes");

/** 設定頁「Default algorithm」選單的選項：label 給人看，value 是 COSE 編號，順序與共用表相同。 */
export const ALGORITHM_OPTIONS: readonly { label: string; value: SupportedAlg }[] =
  SUPPORTED_ALGORITHMS.map((alg) => ({ label: registryEntry(alg).label, value: alg }));
