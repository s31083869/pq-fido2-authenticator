// WASM 版 Falcon 的官方 KAT 測試（Day 7 T6）。
//
// 做什麼：照 NIST PQCgenKAT_sign.c 的流程（liboqs tests/kat_sig.c:740–807 也相同），用 NIST DRBG 取代亂數，
// 讓 extension/public/wasm/pq_bridge.wasm 的 Falcon-512／Falcon-1024 各產生 100 筆，組成官方格式的 .rsp，
// 再和官方 Falcon-Round3.zip 的雜湊（tests/kat/falcon-round3-kat.json）逐筆、整份比對。
// 為什麼：T5 只證明「另一份 liboqs 驗得過」，兩邊同源；KAT 的答案來自 Falcon 原作者的參考實作，
// 才抓得到兩份 liboqs 一起錯、或 WASM 浮點運算結果與原生不同的問題（CLAUDE.md「KAT」）。
// 執行：在專案根目錄 `bun test tests/kat`。
import { describe, expect, test } from "bun:test";
import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";

import { LiboqsWasmBridge, type RandomBytesSource } from "../../extension/src/background/liboqs-wasm-bridge";
import { NistCtrDrbg } from "./nist-drbg";

interface KatEntryHashes {
  count: number;
  seedMsgSha256: string;
  entrySha256: string;
}

interface KatFile {
  sha256: string;
  header: string;
  entries: KatEntryHashes[];
}

// 官方雜湊表：由 compute_falcon_kat_hashes.py 從官方 zip 算出（預期值的來源，不是被測程式）
const OFFICIAL = JSON.parse(
  readFileSync(new URL("./falcon-round3-kat.json", import.meta.url), "utf-8")
) as { algorithms: Record<string, KatFile> };

const WASM_BYTES = readFileSync(new URL("../../extension/public/wasm/pq_bridge.wasm", import.meta.url));

/** bytes → 16 進位大寫（官方 .rsp 的寫法，同 liboqs 的 OQS_fprintBstr）。 */
function hex(bytes: Uint8Array): string {
  return Buffer.from(bytes).toString("hex").toUpperCase();
}

/** 字串（ASCII）的 SHA-256，小寫 16 進位，與 Python hashlib.hexdigest() 相同。 */
function sha256(text: string): string {
  return createHash("sha256").update(text, "ascii").digest("hex");
}

/**
 * 把 liboqs 的 Falcon 簽章轉成官方 KAT 的 sm（signed message）格式。
 *
 * liboqs（Falcon v1.2 第 3.11.3 節）：標頭 0x30+logn ‖ nonce 40 bytes ‖ 壓縮簽章。
 * 官方 sm（參考實作的 NIST API）：簽章長度（2 bytes 大端序，不含 nonce）‖ nonce ‖ msg ‖ 0x20+logn ‖ 壓縮簽章。
 * 依據：liboqs tests/kat_sig.c:65–103 的 combine_message_signature()。
 *
 * @param signature liboqs 的簽章
 * @param message 被簽的訊息
 * @param nistHeader 0x29（Falcon-512）或 0x2A（Falcon-1024）
 * @returns 官方格式的 sm
 */
function toSignedMessage(signature: Uint8Array, message: Uint8Array, nistHeader: number): Uint8Array {
  const nonce = signature.subarray(1, 41);
  const body = signature.subarray(41);
  const lengthWithoutNonce = signature.length - 40;
  const sm = new Uint8Array(2 + signature.length + message.length);
  sm[0] = (lengthWithoutNonce >> 8) & 0xff;
  sm[1] = lengthWithoutNonce & 0xff;
  sm.set(nonce, 2);
  sm.set(message, 42);
  sm[42 + message.length] = nistHeader;
  sm.set(body, 43 + message.length);
  return sm;
}

/**
 * 依官方流程產生一個演算法的 100 筆 KAT。
 *
 * 流程（PQCgenKAT_sign.c）：主 DRBG 以 0..47 初始化；第 i 筆先從主 DRBG 取 48 bytes 當 seed、
 * 再取 33×(i+1) bytes 當 msg；接著用這顆 seed 建立新的 DRBG 供 WASM 使用，產生金鑰、簽章；
 * 主 DRBG 的狀態不受影響（等同 kat_sig.c 的 save_state／restore_state）。
 *
 * @returns 每筆的「seed、mlen、msg」文字與完整 8 行文字
 */
async function generateKat(alg: -54 | -55, nistHeader: number): Promise<Array<{ seedMsg: string; entry: string }>> {
  // WASM 每次要亂數（random_get）時，交給目前這一筆的 DRBG；只有 KAT 測試會這樣做
  let entryDrbg: NistCtrDrbg | null = null;
  const kat: RandomBytesSource = (out) => {
    if (!entryDrbg) {
      throw new Error("WASM asked for randomness outside a KAT entry");
    }
    entryDrbg.fill(out);
  };
  const bridge = await LiboqsWasmBridge.fromBytes(WASM_BYTES, kat);

  const main = new NistCtrDrbg(Uint8Array.from({ length: 48 }, (_, i) => i));
  const results: Array<{ seedMsg: string; entry: string }> = [];

  for (let count = 0; count < 100; count += 1) {
    const seed = main.randomBytes(48);
    const message = main.randomBytes(33 * (count + 1));
    const seedMsg = `seed = ${hex(seed)}\nmlen = ${message.length}\nmsg = ${hex(message)}\n`;

    entryDrbg = new NistCtrDrbg(seed);
    let rest: string;
    try {
      const { publicKey, privateKey } = bridge.generateKeyPair(alg);
      const sm = toSignedMessage(bridge.sign(alg, privateKey, message), message, nistHeader);
      rest = `pk = ${hex(publicKey)}\nsk = ${hex(privateKey)}\nsmlen = ${sm.length}\nsm = ${hex(sm)}\n`;
    } catch (error) {
      // WASM 不支援這個演算法時，仍保留 seed／msg 讓 (a) 能獨立判斷 DRBG 是否正確
      rest = `error = ${String(error)}\n`;
    }
    entryDrbg = null;

    results.push({ seedMsg, entry: `count = ${count}\n${seedMsg}${rest}` });
  }
  return results;
}

describe("WASM Falcon official KAT (Falcon Round 3 v1.2)", () => {
  test.each([
    ["Falcon-512", -54, 0x29],
    ["Falcon-1024", -55, 0x2a]
  ] as const)(
    "T6 %s reproduces the official KAT byte for byte",
    async (title, alg, nistHeader) => {
      const official = OFFICIAL.algorithms[title];
      const generated = await generateKat(alg, nistHeader);
      expect(official.entries).toHaveLength(100);

      // (a) seed、mlen、msg 只由 NIST DRBG 決定：100 筆都和官方相同，證明 DRBG 實作正確
      expect(generated.map((g) => sha256(g.seedMsg))).toEqual(official.entries.map((e) => e.seedMsgSha256));

      // (b) 每一筆完整 8 行（含 pk、sk、sm）都和官方相同；列出第一筆不同的 count 方便除錯
      const mismatched = generated.findIndex((g, i) => sha256(g.entry) !== official.entries[i].entrySha256);
      expect(mismatched).toBe(-1);

      // (c) 依官方格式組出整份 .rsp（標題、空行、每筆後接一個空行），SHA-256 等於官方檔案
      const rsp = `${official.header}\n\n${generated.map((g) => `${g.entry}\n`).join("")}`;
      expect(sha256(rsp)).toBe(official.sha256);
    },
    600_000
  );
});
