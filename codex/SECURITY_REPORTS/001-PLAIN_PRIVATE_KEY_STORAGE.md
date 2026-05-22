# 001 - Plain Private Key Storage in `chrome.storage.local`

## Severity

`High`

## Summary

目前私鑰以 base64 明文存入 extension storage。這會讓「本機被入侵、extension 被利用、資料外流」時的破壞面積直接擴大。

## Affected Code

1. `extension/src/background/authenticator.ts:243`
2. `extension/src/background/store.ts:68`

## Why It Matters

1. 私鑰一旦外洩，攻擊者可離線偽造 assertion。
2. WebAuthn 的核心安全邏輯在於 private key 不可被複製；明文儲存會削弱此保證。

## Attack Scenario

1. 攻擊者取得本機 extension storage（惡意程式、帳號被盜、裝置失守）。
2. 讀出 `privateKey`。
3. 重建簽章流程，對 RP 提交可驗證簽章。

## Recommended Fix

1. 導入 at-rest encryption（AES-GCM）保護儲存內容。
2. 加密金鑰不要與密文同存；至少綁定使用者互動（PIN/UV）或外部信任根。
3. 定義 key rotation 與 migration 流程，避免舊資料永遠用弱模型。

## Verification Checklist

1. storage 中不再出現可直接解讀的 private key 字串。
2. 竄改密文後，系統應拒絕使用（完整性驗證失敗）。
3. 重新啟動 extension 後，合法資料可正常解密簽章。

## Learning Note

對 authenticator 類產品而言，crypto 演算法正確只是基本門檻；key material lifecycle（生成、保存、銷毀）才是安全主體。
