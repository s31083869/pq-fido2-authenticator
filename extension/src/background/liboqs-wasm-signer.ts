import type { SupportedAlg } from "@/types/messages";
import type { GeneratedKeyPair, PQSigner } from "./pq-signer";
import { LiboqsWasmBridge } from "./liboqs-wasm-bridge";

export class LiboqsWasmSigner implements PQSigner {
  private bridgePromise?: Promise<LiboqsWasmBridge>;

  private async bridge(): Promise<LiboqsWasmBridge> {
    if (!this.bridgePromise) {
      this.bridgePromise = LiboqsWasmBridge.loadFromExtensionResource();
    }
    return this.bridgePromise;
  }

  async generateKeyPair(algorithm: SupportedAlg): Promise<GeneratedKeyPair> {
    const bridge = await this.bridge();
    return bridge.generateKeyPair(algorithm);
  }

  async sign(algorithm: SupportedAlg, privateKey: Uint8Array, message: Uint8Array): Promise<Uint8Array> {
    const bridge = await this.bridge();
    return bridge.sign(algorithm, privateKey, message);
  }
}
