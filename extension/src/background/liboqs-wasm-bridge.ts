import type { SupportedAlg } from "@/types/messages";

interface LiboqsWasmExports extends WebAssembly.Exports {
  memory: WebAssembly.Memory;
  malloc(size: number): number;
  free(ptr: number): void;
  pq_public_key_bytes(coseAlg: number): number;
  pq_secret_key_bytes(coseAlg: number): number;
  pq_signature_bytes(coseAlg: number): number;
  pq_generate_keypair(coseAlg: number, publicKeyOut: number, secretKeyOut: number): number;
  pq_sign(
    coseAlg: number,
    secretKey: number,
    secretKeyLen: number,
    message: number,
    messageLen: number,
    signatureOut: number,
    signatureCapacity: number,
    signatureLenOut: number
  ): number;
}

function assertExports(exports: WebAssembly.Exports): asserts exports is LiboqsWasmExports {
  const required = [
    "memory",
    "malloc",
    "free",
    "pq_public_key_bytes",
    "pq_secret_key_bytes",
    "pq_signature_bytes",
    "pq_generate_keypair",
    "pq_sign"
  ] as const;

  for (const key of required) {
    if (!(key in exports)) {
      throw new Error(`[liboqs-wasm] missing export: ${key}`);
    }
  }
}

function copyFromMemory(memory: WebAssembly.Memory, ptr: number, length: number): Uint8Array {
  const view = new Uint8Array(memory.buffer, ptr, length);
  const copy = new Uint8Array(length);
  copy.set(view);
  return copy;
}

export class LiboqsWasmBridge {
  private constructor(private readonly e: LiboqsWasmExports) {}

  static async loadFromExtensionResource(path = "wasm/pq_bridge.wasm"): Promise<LiboqsWasmBridge> {
    const runtime = globalThis.chrome?.runtime;
    if (!runtime?.getURL) {
      throw new Error("[liboqs-wasm] chrome.runtime.getURL is unavailable in this environment");
    }
    const url = runtime.getURL(path);
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`[liboqs-wasm] unable to fetch ${path} (${response.status})`);
    }

    const wasmBytes = await response.arrayBuffer();

    let wasmExports: LiboqsWasmExports | undefined;
    const getMemory = (): WebAssembly.Memory => {
      if (!wasmExports) {
        throw new Error("[liboqs-wasm] memory is not ready");
      }
      return wasmExports.memory;
    };

    const imports = {
      env: {
        emscripten_notify_memory_growth: (_memoryIndex: number): void => {
          // no-op: browser runtime does not need extra handling on growth notifications
        }
      },
      wasi_snapshot_preview1: {
        proc_exit: (code: number): never => {
          throw new Error(`[liboqs-wasm] wasi proc_exit called with code=${code}`);
        },
        random_get: (buf: number, bufLen: number): number => {
          const view = new Uint8Array(getMemory().buffer, buf, bufLen);
          crypto.getRandomValues(view);
          return 0;
        },
        fd_close: (_fd: number): number => {
          return 0;
        },
        fd_seek: (
          _fd: number,
          _offset: bigint,
          _whence: number,
          _newOffsetPtr: number
        ): number => {
          return 0;
        },
        fd_write: (fd: number, _iovs: number, _iovsLen: number, nwritten: number): number => {
          if (fd === 1 || fd === 2) {
            // stdout/stderr output is intentionally ignored in extension runtime.
          }
          new DataView(getMemory().buffer).setUint32(nwritten, 0, true);
          return 0;
        }
      }
    };

    const module = await WebAssembly.instantiate(wasmBytes, imports);
    assertExports(module.instance.exports);
    wasmExports = module.instance.exports;

    return new LiboqsWasmBridge(module.instance.exports);
  }

  publicKeyBytes(alg: SupportedAlg): number {
    const size = this.e.pq_public_key_bytes(alg);
    if (size <= 0) {
      throw new Error(`[liboqs-wasm] invalid public key size for alg=${alg}`);
    }
    return size;
  }

  secretKeyBytes(alg: SupportedAlg): number {
    const size = this.e.pq_secret_key_bytes(alg);
    if (size <= 0) {
      throw new Error(`[liboqs-wasm] invalid secret key size for alg=${alg}`);
    }
    return size;
  }

  signatureBytes(alg: SupportedAlg): number {
    const size = this.e.pq_signature_bytes(alg);
    if (size <= 0) {
      throw new Error(`[liboqs-wasm] invalid signature size for alg=${alg}`);
    }
    return size;
  }

  generateKeyPair(alg: SupportedAlg): { publicKey: Uint8Array; privateKey: Uint8Array } {
    const publicKeyLen = this.publicKeyBytes(alg);
    const privateKeyLen = this.secretKeyBytes(alg);

    const pkPtr = this.e.malloc(publicKeyLen);
    const skPtr = this.e.malloc(privateKeyLen);

    try {
      const rc = this.e.pq_generate_keypair(alg, pkPtr, skPtr);
      if (rc !== 0) {
        throw new Error(`[liboqs-wasm] pq_generate_keypair failed with code=${rc}`);
      }

      return {
        publicKey: copyFromMemory(this.e.memory, pkPtr, publicKeyLen),
        privateKey: copyFromMemory(this.e.memory, skPtr, privateKeyLen)
      };
    } finally {
      this.e.free(pkPtr);
      this.e.free(skPtr);
    }
  }

  sign(alg: SupportedAlg, privateKey: Uint8Array, message: Uint8Array): Uint8Array {
    const expectedSkLen = this.secretKeyBytes(alg);
    if (privateKey.length !== expectedSkLen) {
      throw new Error(
        `[liboqs-wasm] secret key length mismatch for alg=${alg}: got=${privateKey.length}, expected=${expectedSkLen}`
      );
    }

    const sigCap = this.signatureBytes(alg);

    const skPtr = this.e.malloc(privateKey.length);
    const msgPtr = this.e.malloc(message.length);
    const sigPtr = this.e.malloc(sigCap);
    const sigLenPtr = this.e.malloc(4);

    try {
      new Uint8Array(this.e.memory.buffer, skPtr, privateKey.length).set(privateKey);
      new Uint8Array(this.e.memory.buffer, msgPtr, message.length).set(message);
      new DataView(this.e.memory.buffer).setUint32(sigLenPtr, 0, true);

      const rc = this.e.pq_sign(
        alg,
        skPtr,
        privateKey.length,
        msgPtr,
        message.length,
        sigPtr,
        sigCap,
        sigLenPtr
      );
      if (rc !== 0) {
        throw new Error(`[liboqs-wasm] pq_sign failed with code=${rc}`);
      }

      const sigLen = new DataView(this.e.memory.buffer).getUint32(sigLenPtr, true);
      if (sigLen === 0 || sigLen > sigCap) {
        throw new Error(`[liboqs-wasm] invalid signature length: ${sigLen}`);
      }

      return copyFromMemory(this.e.memory, sigPtr, sigLen);
    } finally {
      this.e.free(skPtr);
      this.e.free(msgPtr);
      this.e.free(sigPtr);
      this.e.free(sigLenPtr);
    }
  }
}
