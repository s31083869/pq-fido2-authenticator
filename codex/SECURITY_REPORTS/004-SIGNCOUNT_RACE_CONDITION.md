# 004 - `signCount` Race Condition on Concurrent Assertions

## Severity

`Medium`

## Summary

assertion 流程先讀取 `signCount` 再寫回，缺少鎖或原子更新機制。並發請求可能產生相同 counter。

## Affected Code

1. `extension/src/background/authenticator.ts:281`
2. `extension/src/background/authenticator.ts:290`
3. `extension/src/background/authenticator.ts:301`

## Why It Matters

1. RP 常以 counter 單調遞增檢測 cloned authenticator。
2. 重複 counter 可能觸發風險告警，或使偵測機制失效。

## Attack / Failure Scenario

1. 同 credential 同時送兩個 `get`。
2. 兩個流程都讀到相同舊值 `N`。
3. 兩邊都產出 `N+1` 並覆蓋，造成重複 counter。

## Recommended Fix

1. 針對 credentialId 建立 per-key mutex。
2. 進入 critical section 後重新讀取、遞增、簽章、提交。
3. 確保寫回失敗時不回傳成功 assertion。

## Verification Checklist

1. 壓測並發 assertion，不再出現重複 counter。
2. counter 必須保持嚴格單調遞增。
3. race 測試納入 CI。

## Learning Note

任何「讀-改-寫」狀態欄位都要先假設有並發；signCount 是典型教材案例。
