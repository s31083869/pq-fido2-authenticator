## 🧩 Clarify

### 專案目的
建立一個以 **Python Authenticator** 為核心、支援 **Post-Quantum Cryptography (PQC)** 的 FIDO2 認證系統，  
可於 macOS 平台完成標準 WebAuthn 註冊與登入流程。  
專案以 **研究性質 (PoC)** 為主，重點在於驗證 ML-DSA 系列演算法與 FIDO2 流程的整合可行性。

### 系統組成
1. **Frontend (Next.js)**  
   - 使用 `navigator.credentials` API 與 RP Server 溝通。  
   - 使用 `react-hook-form` + `zod` 進行資料驗證與型別安全控制。  
   - 顯示註冊／登入 UI 流程與錯誤提示。  

2. **RP Server (Flask)**  
   - 實作標準 WebAuthn RP API：`/register/options`, `/register/verify`, `/authenticate/options`, `/authenticate/verify`。  
   - 使用 `liboqs-python` 驗證 ML-DSA PQC 簽章。  
   - 使用 `SQLAlchemy` 儲存 user 與 credential 資料。  

3. **Authenticator (Python)**  
   - 攔截 `navigator.credentials.create/get` 流程。  
   - 使用 `Playwright` 控制 Chromium 並攔截 JS。  
   - 使用 `pyobjc` 呼叫 Touch ID 驗證使用者。  
   - 使用 `liboqs-python` 產生 ML-DSA 公私鑰對。  
   - 使用 `keyring` 將私鑰安全儲存在 macOS Keychain。  
   - 回傳模擬的 Authenticator Response 結構（JSON / Base64 格式）。  

---

## 🧭 Plan

### 階段 1：開發環境與框架建立
- [x] 設定 Python 專案結構與 `uv` 管理套件。
- [x] 初始化 Flask 專案，建立基本 API 結構。
- [x] 建立 Next.js 專案，設定 Shadcn UI 與 `zod` 驗證。
- [x] 建立 Playwright 測試環境與 Chromium 控制腳本。

### 階段 2：Authenticator 實作
- [x] 實作 `Authenticator` 類別：
  - [x] `make_credential()`：模擬註冊流程。
  - [x] `get_assertion()`：模擬登入流程。
- [x] 整合 `liboqs-python`，支援 ML-DSA-44 / 65 / 87。
- [x] 整合 `pyobjc` 呼叫 Touch ID 作為 User Verification。
- [x] 整合 `keyring` 進行憑證儲存與讀取。
- [x] 實作輸出 JSON 結構（對應 RP Server 驗證欄位）。

### 階段 3：RP Server 實作
- [x] 建立資料模型（User / Credential）。
- [x] 實作 `/register/options` 與 `/register/verify`。
- [x] 實作 `/authenticate/options` 與 `/authenticate/verify`。
- [x] 使用 `liboqs-python` 驗證簽章正確性。
- [x] 確保 RP Server 可處理自定 JSON/Base64 結構（非 CBOR）。

### 階段 4：Frontend 實作
- [x] 建立註冊頁面與登入頁面。
- [x] 使用 `navigator.credentials.create/get` 與 RP API 互動。
- [x] 使用 `zod` 驗證資料型別。
- [x] 顯示 Touch ID 驗證提示與狀態。
- [x] 顯示後量子安全標示（Post-Quantum Secure）。

### 階段 5：測試與整合
- [x] 使用 `pytest` 撰寫 Authenticator 與 RP 單元測試。
- [x] 使用 `bun:test` 撰寫前端表單邏輯測試。
- [x] 使用 Playwright 進行端對端（E2E）註冊／登入流程測試。
- [ ] 驗證與 [Yubico Demo](https://demo.yubico.com/webauthn-developers) 兼容性。

---

## ⚠️ Risk

| 類別 | 風險 | 對應策略 |
|------|------|-----------|
| **格式不相容** | python-fido2 預期使用 CBOR/COSE，而此實作以 JSON 包裝 | RP Server 層建立 JSON→CBOR 轉換器或自訂驗證模組 |
| **Touch ID 限制** | `pyobjc` 可能受 macOS 權限限制 | 使用 LocalAuthentication API 並設定權限 |
| **liboqs 演算法穩定性** | PQC 實驗性實作可能導致相容性問題 | 鎖定 `liboqs` 版本，使用 ML-DSA 系列 |
| **瀏覽器攔截可靠性** | Chromium API 更新可能影響 Playwright 攔截 | 寫入自動化測試監控 navigator.credentials 攔截狀態 |
| **資料安全** | Keychain 存取權限與安全設定不正確 | 使用 `kSecAttrAccessibleWhenUnlocked` 並測試存取權限 |

---

## 🔌 Interface

### Authenticator ↔ RP Server
| 流程 | Request | Response |
|------|----------|-----------|
| 註冊 (Create) | `PublicKeyCredentialCreationOptions` | `AuthenticatorAttestationResponse (JSON)` |
| 登入 (Get) | `PublicKeyCredentialRequestOptions` | `AuthenticatorAssertionResponse (JSON)` |

### Authenticator ↔ 系統模組
| 模組 | 職責 |
|------|------|
| **Playwright** | 攔截並注入 JS (navigator.credentials.create/get) |
| **pyobjc** | 呼叫 macOS Touch ID (LocalAuthentication) |
| **liboqs-python** | 生成與驗證 ML-DSA 簽章 |
| **keyring** | 儲存與讀取私鑰憑證 |

### RP Server ↔ Frontend
| Endpoint | 描述 |
|-----------|------|
| `/register/options` | RP 產生 challenge 與註冊參數 |
| `/register/verify` | 驗證 Authenticator attestation |
| `/authenticate/options` | RP 產生登入挑戰 |
| `/authenticate/verify` | 驗證 Authenticator assertion |

---

### 資料流摘要
```text
[Frontend] navigator.credentials.create()
   ↓
[Authenticator (Python)]
   ├─ pyobjc → Touch ID
   ├─ liboqs → 產生 PQC Key
   └─ keyring → 儲存憑證
   ↓
[RP Server (Flask)] 驗證 challenge + 簽章
```
