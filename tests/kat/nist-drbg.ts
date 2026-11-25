// NIST PQC 的決定性亂數產生器（AES-256 CTR DRBG），用來重現官方 KAT（Day 7 T6）。
//
// 為什麼：官方 KAT 檔是 NIST 的 PQCgenKAT_sign.c 搭配 rng.c 的 randombytes() 產生的；同一顆種子，
// 永遠吐出同一串 bytes。用它取代 WASM 的亂數來源，Falcon 的金鑰與簽章就能和官方答案逐 byte 比對。
// 依據：NIST PQC 提交包附的 rng.c（AES256_CTR_DRBG_Update、randombytes_init、randombytes）；
// liboqs tests/kat_sig.c 也以同樣的 DRBG 產生 KAT。
//
// 這個 DRBG 只能用在測試：輸出完全可預測，用來產生真的金鑰等於公開私鑰。
// 它本身也是被測的程式，但它產生的每筆 seed 與 msg 就在官方檔案裡，寫錯時 T6 (a) 一定失敗。
import { createCipheriv } from "node:crypto";

/**
 * NIST AES-256 CTR DRBG（rng.c）的 TypeScript 版本。
 *
 * 做什麼：以 48 bytes 種子初始化後，每次 fill()／randomBytes() 都依 rng.c 的規則產生下一段 bytes。
 * 為什麼：T6 用它取代 WASM 的亂數，讓 Falcon 的輸出可以和官方 KAT 逐 byte 比對。
 * 輸入與輸出：建構時給種子；之後每次呼叫回傳（或填入）指定長度的 bytes。
 */
export class NistCtrDrbg {
  /** AES-256 金鑰（rng.c 的 DRBG_ctx.Key） */
  private key = new Uint8Array(32);
  /** 計數器（rng.c 的 DRBG_ctx.V），每產生一個 AES 區塊前先加 1 */
  private v = new Uint8Array(16);

  /**
   * 對應 rng.c 的 randombytes_init(entropy_input, personalization_string, 256)。
   *
   * @param entropy 48 bytes 的種子（官方 KAT 一開始用 0, 1, …, 47；每筆再用該筆的 seed）
   * @param personalization 選用的 48 bytes 個人化字串，會和種子做 XOR（官方 KAT 不使用）
   * @throws Error 種子或個人化字串不是 48 bytes
   */
  constructor(entropy: Uint8Array, personalization?: Uint8Array) {
    if (entropy.length !== 48 || (personalization && personalization.length !== 48)) {
      throw new Error("NIST CTR DRBG needs a 48-byte seed");
    }
    const seedMaterial = Uint8Array.from(entropy);
    if (personalization) {
      for (let i = 0; i < 48; i += 1) {
        seedMaterial[i] ^= personalization[i];
      }
    }
    this.update(seedMaterial);
  }

  /** 用目前的金鑰對一個 16 bytes 區塊做 AES-256-ECB 加密（rng.c 的 AES256_ECB）。 */
  private aes(block: Uint8Array): Uint8Array {
    const cipher = createCipheriv("aes-256-ecb", this.key, null);
    cipher.setAutoPadding(false);
    return new Uint8Array(cipher.update(block));
  }

  /** V 視為 128 位元大端序整數加 1，溢位時從最低位元組往前進位。 */
  private incrementV(): void {
    for (let j = 15; j >= 0; j -= 1) {
      if (this.v[j] === 0xff) {
        this.v[j] = 0x00;
      } else {
        this.v[j] += 1;
        break;
      }
    }
  }

  /**
   * rng.c 的 AES256_CTR_DRBG_Update：產生 3 個區塊（48 bytes），與 provided 做 XOR 後，
   * 前 32 bytes 成為新的金鑰、後 16 bytes 成為新的 V。
   */
  private update(provided?: Uint8Array): void {
    const temp = new Uint8Array(48);
    for (let i = 0; i < 3; i += 1) {
      this.incrementV();
      temp.set(this.aes(this.v), 16 * i);
    }
    if (provided) {
      for (let i = 0; i < 48; i += 1) {
        temp[i] ^= provided[i];
      }
    }
    this.key = temp.slice(0, 32);
    this.v = temp.slice(32, 48);
  }

  /**
   * rng.c 的 randombytes(x, xlen)：把 out 整段填滿，結束後更新一次內部狀態。
   *
   * 注意：一次要 n + m bytes 與分兩次各要 n、m bytes 的結果不同（每次呼叫結束都會更新狀態），
   * 所以呼叫的切法必須和官方流程一致。
   */
  fill(out: Uint8Array): void {
    for (let offset = 0; offset < out.length; offset += 16) {
      this.incrementV();
      const block = this.aes(this.v);
      out.set(block.subarray(0, Math.min(16, out.length - offset)), offset);
    }
    this.update();
  }

  /** 取得 n 個 bytes（等同對新的陣列呼叫一次 fill）。 */
  randomBytes(n: number): Uint8Array {
    const out = new Uint8Array(n);
    this.fill(out);
    return out;
  }
}
