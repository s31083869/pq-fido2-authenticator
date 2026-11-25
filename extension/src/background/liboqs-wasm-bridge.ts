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

/**
 * 亂數來源：把 `out` 整段填滿亂數 bytes。
 *
 * liboqs 產生金鑰與簽章時需要的亂數，在 WASM 裡會經由 WASI 的 random_get 交給這個函式。
 */
export type RandomBytesSource = (out: Uint8Array) => void;

/**
 * 預設的亂數來源：瀏覽器與 bun 都有的 Web Crypto（CSPRNG）。
 *
 * getRandomValues() 一次最多填 65,536 bytes，所以分段填；liboqs 每次要的亂數遠小於這個上限。
 */
const systemRandomBytes: RandomBytesSource = (out) => {
  for (let offset = 0; offset < out.length; offset += 65_536) {
    crypto.getRandomValues(out.subarray(offset, Math.min(offset + 65_536, out.length)));
  }
};

/**
 * pq_bridge.wasm（C 編譯成 WebAssembly 的 liboqs）的 TypeScript 包裝。
 *
 * 做什麼：在 WASM 的線性記憶體裡配置緩衝區、呼叫 C 匯出的函式、把結果複製回 JavaScript。
 * 為什麼：Extension 的簽章器（liboqs-wasm-signer.ts）透過它在瀏覽器裡產生後量子金鑰與簽章，
 * 使用者不需要安裝原生的 liboqs。C 端的 COSE → liboqs 對應見 extension/wasm/pq_bridge.c。
 */
export class LiboqsWasmBridge {
  private constructor(private readonly e: LiboqsWasmExports) {}

  /**
   * 在 Extension 裡載入打包好的 pq_bridge.wasm（manifest 的 web_accessible 資源）。
   *
   * 做什麼：用 chrome.runtime.getURL() 取得資源網址、fetch 下來，再交給 fromBytes() 建立 bridge。
   * 只能在 Extension 環境呼叫；測試環境沒有 chrome，請直接用 fromBytes()。
   *
   * @param path 相對於 Extension 根目錄的 WASM 路徑
   * @returns 可以呼叫 liboqs 的 bridge，亂數一律用系統 CSPRNG
   * @throws Error chrome.runtime 不存在，或 fetch 失敗
   */
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

    return LiboqsWasmBridge.fromBytes(await response.arrayBuffer());
  }

  /**
   * 從 WASM 檔案的 bytes 建立 bridge。
   *
   * 為什麼拆出來：bun 測試沒有 chrome.runtime，要直接讀 public/wasm/pq_bridge.wasm 才能測到真的 liboqs（Day 7）。
   *
   * pq_bridge.wasm 以 STANDALONE_WASM 編譯，需要少數 WASI 匯入：random_get 供應亂數，
   * fd_write 等輸出函式在 Extension 裡不需要，直接忽略。
   *
   * @param wasmBytes pq_bridge.wasm 的內容
   * @param randomBytes 亂數來源。**只有 KAT 測試會傳入決定性的 NIST DRBG**，讓輸出可以和官方答案逐 byte 比對；
   *   Extension 從不傳這個參數，一律使用系統 CSPRNG。傳入可預測的亂數會讓私鑰與簽章可被重現，絕不能用在實際流程
   * @returns 可以呼叫 liboqs 的 bridge
   * @throws WebAssembly.CompileError wasmBytes 不是合法的 WASM
   * @throws WebAssembly.LinkError WASM 需要的匯入與這裡提供的不符
   * @throws Error WASM 缺少必要的匯出函式
   */
  static async fromBytes(
    wasmBytes: BufferSource,
    randomBytes: RandomBytesSource = systemRandomBytes
  ): Promise<LiboqsWasmBridge> {
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
          // 記憶體擴充通知：瀏覽器端不需要額外處理（每次存取都重新取 memory.buffer）
        }
      },
      wasi_snapshot_preview1: {
        proc_exit: (code: number): never => {
          throw new Error(`[liboqs-wasm] wasi proc_exit called with code=${code}`);
        },
        // liboqs 的 OQS_randombytes() 在 WASM 裡最後會呼叫這裡；每次呼叫填滿 [buf, buf + bufLen)
        random_get: (buf: number, bufLen: number): number => {
          randomBytes(new Uint8Array(getMemory().buffer, buf, bufLen));
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
        // stdout／stderr 的輸出在 Extension 裡刻意忽略，只回報寫入 0 bytes
        fd_write: (_fd: number, _iovs: number, _iovsLen: number, nwritten: number): number => {
          new DataView(getMemory().buffer).setUint32(nwritten, 0, true);
          return 0;
        }
      }
    };

    // 先 compile 再 instantiate：明確拿到 Instance，型別不受 instantiate() 多載的影響
    const module = await WebAssembly.compile(wasmBytes);
    const instance = await WebAssembly.instantiate(module, imports);
    assertExports(instance.exports);
    wasmExports = instance.exports;

    return new LiboqsWasmBridge(instance.exports);
  }

  /**
   * 向 WASM 查詢公鑰大小（liboqs 的 length_public_key）。
   *
   * C 端回傳負值代表錯誤，錯誤訊息會帶出這個代碼，方便分辨原因（見 pq_bridge.c）：
   * -1：pq_alg_name() 沒有這個 COSE 編號；-2：有對應名稱，但 liboqs.a 沒有編進這個演算法。
   *
   * @param alg COSE 演算法編號
   * @returns 公鑰大小（bytes）
   * @throws Error C 端回傳 0 或負值，訊息含 code=<回傳值>
   */
  publicKeyBytes(alg: SupportedAlg): number {
    const size = this.e.pq_public_key_bytes(alg);
    if (size <= 0) {
      throw new Error(`[liboqs-wasm] invalid public key size for alg=${alg} (code=${size})`);
    }
    return size;
  }

  /**
   * 向 WASM 查詢私鑰大小（liboqs 的 length_secret_key）。錯誤代碼同 publicKeyBytes()。
   *
   * @param alg COSE 演算法編號
   * @returns 私鑰大小（bytes）
   * @throws Error C 端回傳 0 或負值，訊息含 code=<回傳值>
   */
  secretKeyBytes(alg: SupportedAlg): number {
    const size = this.e.pq_secret_key_bytes(alg);
    if (size <= 0) {
      throw new Error(`[liboqs-wasm] invalid secret key size for alg=${alg} (code=${size})`);
    }
    return size;
  }

  /**
   * 向 WASM 查詢簽章大小（liboqs 的 length_signature）。錯誤代碼同 publicKeyBytes()。
   *
   * ML-DSA 是固定長度；FN-DSA（不補滿格式）是上限，只用來配置緩衝區，實際長度由 sign() 取得。
   *
   * @param alg COSE 演算法編號
   * @returns 簽章大小或上限（bytes）
   * @throws Error C 端回傳 0 或負值，訊息含 code=<回傳值>
   */
  signatureBytes(alg: SupportedAlg): number {
    const size = this.e.pq_signature_bytes(alg);
    if (size <= 0) {
      throw new Error(`[liboqs-wasm] invalid signature size for alg=${alg} (code=${size})`);
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
