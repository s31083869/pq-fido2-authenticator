# 006 - Production Sourcemap Exposure

## Severity

`Low`

## Summary

目前 build 設定在輸出包中保留 sourcemap。這會降低攻擊者逆向成本，增加程式結構暴露面。

## Affected Code

1. `extension/vite.config.ts:16`

## Why It Matters

1. 攻擊者可更快定位邏輯節點（bridge、storage、signer）。
2. 安全繞過與漏洞利用成本降低。

## Recommended Fix

1. release build 關閉 sourcemap。
2. 若需除錯，改為 internal-only debug build（不發佈）。

## Verification Checklist

1. release artifact 不包含 `.map`。
2. debug/release 配置明確分離。

## Learning Note

sourcemap 本身不是漏洞，但在攻防上等於「送出高品質導航圖」。
