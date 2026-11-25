# `public/wasm/`

Generated wasm output directory.

## Artifact

1. `pq_bridge.wasm`

## How to Generate

```bash
bun run setup:liboqs:wasm
bun run build:wasm
```

## Runtime Use

1. loaded via `chrome.runtime.getURL("wasm/pq_bridge.wasm")`
2. consumed by background service worker only

## Tests

這個檔案有進 git，下列測試直接讀它（Day 7）：

1. `src/background/liboqs-wasm-bridge.test.ts`：大小、金鑰、簽章格式
2. `tests/integration/test_wasm_cross_verify.py`：WASM 簽章交給 RP 的 Python liboqs 驗章
3. `tests/kat/wasm-falcon-kat.test.ts`：Falcon 官方 KAT

重建後三者都必須通過。
