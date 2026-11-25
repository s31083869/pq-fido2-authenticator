// 用真的 pq_bridge.wasm 對每個演算法產生一把金鑰、簽一則固定訊息，把結果輸出成 JSON（Day 7 T5）。
//
// 為什麼：Extension（WASM 版 liboqs，33815beb）與 RP（原生 liboqs 0.14.0）是兩份分別編譯的實作。
// tests/integration/test_wasm_cross_verify.py 會執行這個腳本，再用 RP 的演算法對照與 Python liboqs 驗章，
// 證明 WASM 簽出來的簽章，RP 那一邊真的驗得過（CLAUDE.md「真實密碼學」：產生金鑰 → 簽章 → RP 驗章）。
//
// 用法：bun extension/scripts/wasm-sign-vectors.ts [WASM 檔路徑]
//   不給路徑時，讀 extension/public/wasm/pq_bridge.wasm（進 git 的那一份）。
// 輸出（stdout）：JSON 陣列，每個演算法一筆：
//   成功 {"alg": -54, "publicKey": "<base64>", "message": "<base64>", "signature": "<base64>"}
//   失敗 {"alg": -54, "error": "<訊息>"}（例如 WASM 沒編進這個演算法）；失敗不中斷，讓測試指出是哪一個。
import { readFileSync } from "node:fs";

import { SUPPORTED_ALGORITHMS } from "../src/lib/algorithms";
import { LiboqsWasmBridge } from "../src/background/liboqs-wasm-bridge";

const wasmPath = process.argv[2] ?? new URL("../public/wasm/pq_bridge.wasm", import.meta.url);

// 固定訊息：模擬 WebAuthn 登入時被簽的資料長度（authData 37 bytes ‖ SHA-256(clientDataJSON) 32 bytes = 69 bytes），
// 內容是可重現的 0, 1, 2, …，方便除錯時比對
const MESSAGE = Uint8Array.from({ length: 69 }, (_, i) => i);

/** 把 bytes 轉成標準 base64（Python 端用 base64.b64decode 解回來）。 */
function toBase64(bytes: Uint8Array): string {
  return Buffer.from(bytes).toString("base64");
}

/**
 * 對每個支援的演算法各做一次「產生金鑰 → 簽章」。
 *
 * 每個演算法用全新的 WASM 實例：某個演算法若破壞了 WASM 的記憶體（例如堆疊越界），不會影響下一個的結果。
 *
 * @returns 每個演算法一筆結果，順序與共用演算法表相同
 */
async function main(): Promise<void> {
  const wasmBytes = readFileSync(wasmPath);
  const results: Array<Record<string, string | number>> = [];

  for (const alg of SUPPORTED_ALGORITHMS) {
    try {
      const bridge = await LiboqsWasmBridge.fromBytes(wasmBytes);
      const { publicKey, privateKey } = bridge.generateKeyPair(alg);
      const signature = bridge.sign(alg, privateKey, MESSAGE);
      results.push({
        alg,
        publicKey: toBase64(publicKey),
        message: toBase64(MESSAGE),
        signature: toBase64(signature)
      });
    } catch (error) {
      results.push({ alg, error: String(error) });
    }
  }

  process.stdout.write(JSON.stringify(results));
}

await main();
