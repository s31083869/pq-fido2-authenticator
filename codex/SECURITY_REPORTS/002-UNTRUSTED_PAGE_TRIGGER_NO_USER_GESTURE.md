# 002 - Untrusted Page Script Can Trigger Signing Flow Without User Gesture

## Severity

`High`

## Summary

只要腳本在目標頁面上下文中執行（含第三方腳本/XSS），即可透過 bridge 觸發 create/get 流程。當前流程缺少「明確使用者操作確認」。

## Affected Code

1. `extension/src/injected/index.ts:164`
2. `extension/src/injected/index.ts:176`
3. `extension/src/content/index.ts:24`
4. `extension/src/content/index.ts:50`

## Why It Matters

1. 目前只做「網域限制」，未做「操作意圖限制」。
2. 若頁面被注入惡意 JS，可在背景悄悄發動註冊或認證請求。

## Attack Scenario

1. `demo.yubico.com` 頁面出現 XSS/惡意第三方 script。
2. 惡意 script 呼叫被 hook 的 `navigator.credentials.get/create`。
3. extension 執行簽章流程並回傳憑證資料，使用者無感。

## Recommended Fix

1. 加入 per-request 使用者確認（至少一次 click-confirm）。
2. 強制 user-gesture gate（如最近互動時間窗）。
3. 加入 request throttling 與 request origin/session 綁定。

## Verification Checklist

1. 無使用者操作時，request 必須被拒絕。
2. 有使用者明確確認後，request 才能進入 signer。
3. 自動化惡意腳本重放時，會被策略攔截。

## Learning Note

「同網域」不等於「可信呼叫者」。安全邊界應建立在使用者意圖而非僅 host name。
