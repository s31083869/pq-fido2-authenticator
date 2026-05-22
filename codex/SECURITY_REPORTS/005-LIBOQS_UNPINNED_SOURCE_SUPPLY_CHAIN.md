# 005 - Unpinned `liboqs` Source (Supply Chain Reproducibility Risk)

## Severity

`Medium`

## Summary

目前 build script 預設使用 `liboqs main`。此設定會讓不同時間建置得到不同結果，增加供應鏈風險與除錯成本。

## Affected Code

1. `extension/scripts/setup-liboqs-emscripten.sh:10`
2. `extension/scripts/setup-liboqs-emscripten.sh:49`

## Why It Matters

1. `main` 分支會持續變動，可能引入未預期行為。
2. 安全事件發生時，難以回溯「當時實際編譯內容」。

## Recommended Fix

1. 預設改為固定 tag 或 commit SHA。
2. 在報告與 artifact 中記錄：
   1. `liboqs` commit
   2. 編譯參數
   3. wasm 輸出 hash
3. 可加 `verify` 腳本做 hash/checksum 驗證。

## Verification Checklist

1. 同 commit 反覆建置得到可重現輸出（或可解釋差異）。
2. PR 中能清楚審閱「升級哪個 liboqs 版本」。

## Learning Note

供應鏈安全不是只有「有沒有漏洞」，還包含「你能不能準確說明自己到底部署了什麼」。
