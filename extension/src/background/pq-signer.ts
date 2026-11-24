import type { SupportedAlg } from "@/types/messages";

// 金鑰與簽章的大小常數改由共用演算法表產生（決策 D3、workflow.md F10），這裡只轉出，
// 讓既有的 import 路徑不變。FN-DSA 的 SIGNATURE_BYTES 是上限而不是固定長度，說明見 @/lib/algorithms。
export { PRIVATE_KEY_BYTES, PUBLIC_KEY_BYTES, SIGNATURE_BYTES } from "@/lib/algorithms";

export interface GeneratedKeyPair {
  publicKey: Uint8Array;
  privateKey: Uint8Array;
}

export interface PQSigner {
  generateKeyPair(algorithm: SupportedAlg): Promise<GeneratedKeyPair>;
  sign(algorithm: SupportedAlg, privateKey: Uint8Array, message: Uint8Array): Promise<Uint8Array>;
}
