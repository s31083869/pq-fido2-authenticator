import type { SupportedAlg } from "@/types/messages";

export const PUBLIC_KEY_BYTES: Record<SupportedAlg, number> = {
  [-48]: 1312,
  [-49]: 1952,
  [-50]: 2592
};

export const PRIVATE_KEY_BYTES: Record<SupportedAlg, number> = {
  [-48]: 2560,
  [-49]: 4032,
  [-50]: 4896
};

export const SIGNATURE_BYTES: Record<SupportedAlg, number> = {
  [-48]: 2420,
  [-49]: 3309,
  [-50]: 4627
};

export interface GeneratedKeyPair {
  publicKey: Uint8Array;
  privateKey: Uint8Array;
}

export interface PQSigner {
  generateKeyPair(algorithm: SupportedAlg): Promise<GeneratedKeyPair>;
  sign(algorithm: SupportedAlg, privateKey: Uint8Array, message: Uint8Array): Promise<Uint8Array>;
}
