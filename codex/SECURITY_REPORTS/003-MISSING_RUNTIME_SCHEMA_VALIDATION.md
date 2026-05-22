# 003 - Missing Runtime Schema Validation on Message Boundary

## Severity

`Medium`

## Summary

背景層處理 bridge message 時，缺少嚴格 runtime schema validation。這會放大 malformed input、邏輯繞過與未預期行為風險。

## Affected Code

1. `extension/src/background/index.ts:55`
2. `extension/src/background/index.ts:58`
3. `extension/src/background/index.ts:63`

## Why It Matters

1. TS 型別只在編譯時有效，無法保證執行期輸入安全。
2. `message.action` 若非 `create`，目前會直接走 `get` 路徑。
3. payload 長度/欄位結構未限制，可能導致 DoS 或邏輯偏差。

## Recommended Fix

1. 在 message 入口加 schema 驗證（`zod` 很適合）。
2. 對 `action` 做枚舉白名單，未知值直接拒絕。
3. 對 binary-like 字串長度做上限檢查（challenge、id、userHandle）。

## Verification Checklist

1. 非法 `action` 會回傳 `TypeError/DataError`。
2. 缺欄位或型別錯誤的 payload 不會進入 authenticator。
3. 超大 payload 會被拒絕而不影響 service worker 穩定性。

## Learning Note

驗證邊界輸入是安全工程最划算的一步。`zod` 的價值在於「把規格變成可執行防線」。
