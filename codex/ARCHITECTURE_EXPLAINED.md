# PQ-FIDO2-Authenticator 架構詳解

## 概述
這是一個後量子密碼學 (Post-Quantum Cryptography) FIDO2 認證器實現，包含 Python 後端服務、Playwright 測試橋接和 TypeScript 瀏覽器擴展。

---

## 1️⃣ 核心架構流程圖

```
用戶在瀏覽器中操作 (localhost:3000)
         ↓
JavaScript 攔截 navigator.credentials.create/get
         ↓
Playwright Bridge (JavaScript 注入腳本)
         ↓
暴露 Python 綁定:
  ✓ __pqMakeCredential
  ✓ __pqGetAssertion  
  ✓ __pqListCredentials
         ↓
Python Authenticator Service
  ✓ 生成 ML-DSA 密鑰對
  ✓ 簽署斷言
  ✓ 存儲憑證
         ↓
返回簽名響應給瀏覽器
         ↓
RP Server 驗證 (Flask)
```

---

## 2️⃣ Playwright Bridge 運作方式

### 目的
Playwright Bridge 是一個 Python 層，攔截並模擬瀏覽器中的 WebAuthn 調用。

### 核心文件
- **[authenticator/bridge.py](authenticator/bridge.py)** — Playwright 集成的主要邏輯
- **[authenticator/__main__.py](authenticator/__main__.py)** — CLI 入口點

### 執行流程

**1. 啟動** 
```bash
python -m authenticator --url http://localhost:3000
```

**2. 初始化**
```python
async def run(self):
    async with async_playwright() as playwright:
        # 啟動 Chromium (headless=False，允許視覺交互)
        browser = await playwright.chromium.launch(headless=False)
        context = await browser.new_context()
        
        # 注入 JavaScript 攔截腳本
        await context.add_init_script(INJECT_SCRIPT)
        
        # 暴露 Python 綁定給 JavaScript
        await context.expose_binding("__pqMakeCredential", self._handle_make)
        await context.expose_binding("__pqGetAssertion", self._handle_get)
```

**3. 注入的 JavaScript 腳本**（在 [bridge.py#L17-L160](authenticator/bridge.py#L17-L160)）

腳本會：
- 攔截全局 `navigator.credentials` 對象
- 監聽 `.create()` 和 `.get()` 調用
- 將 ArrayBuffer 轉換為 Base64URL（JSON 可序列化）
- 調用暴露的 Python 綁定

**關鍵代碼片段：**
```javascript
// 在 JavaScript 中
const response = await window.__pqMakeCredential({
  publicKey: {
    challenge: bufferToBase64url(options.publicKey.challenge),
    rp: options.publicKey.rp,
    user: {
      id: bufferToBase64url(options.publicKey.user.id),
      name: options.publicKey.user.name,
      // ...
    }
  }
});
// 返回 Python 簽署的響應
```

**4. Python 側處理**
```python
async def _handle_make(self, source, payload):
    # payload 包含 Base64URL 編碼的數據
    response = self.authenticator.make_credential(
        options_data=payload,
        origin=source.url
    )
    # 返回 Base64URL 編碼的簽署響應
    return response
```

### 關鍵特性
| 特性 | 說明 |
|------|------|
| **異步** | 使用 `asyncio` 和 `async/await` |
| **無頭控制** | Playwright 完全控制瀏覽器自動化 |
| **Buffer 序列化** | ArrayBuffer ↔ Base64URL 自動轉換 |
| **沙箱隔離** | Python 邏輯完全與 JavaScript 分離 |

---

## 3️⃣ Extension 運作方式

### 目的
Browser Extension 是一個獨立的元件，模擬瀏覽器中的認證器行為。它不直接與 Playwright Bridge 集成。

### 文件結構
```
extension/
├── src/background/
│   ├── authenticator.ts      ← 核心認證器邏輯
│   ├── pq-signer.ts          ← 簽署實現
│   ├── liboqs-wasm-signer.ts ← WASM 密碼原語
│   ├── store.ts              ← Chrome Storage 封裝
│   ├── authenticator.test.ts ← 單元測試
│   └── store.test.ts         ← 存儲測試
├── public/
│   └── manifest.json         ← Extension 宣言
└── src/options/              ← 設置頁面 UI
```

### 核心類：PQAuthenticator

**初始化**
```typescript
const authenticator = new PQAuthenticator(settings, store);
```

**主要方法**
```typescript
// 創建憑證
create(options: PublicKeyCredentialCreationOptions): Promise<AuthenticatorAttestationResponse>

// 獲取斷言（簽署）
get(options: PublicKeyCredentialRequestOptions): Promise<AuthenticatorAssertionResponse>

// 列出存儲的憑證
listCredentials(): Promise<PublicKeyCredentialDescriptor[]>
```

**工作流程**
```
1. RP Server 發送挑戰 (Challenge)
2. Extension 接收 credential creation options
3. 生成 ML-DSA-44/65/87 密鑰對
4. 簽署認證數據
5. 返回認證器證明對象給 RP
6. RP 驗證簽署
```

### 測試方法

所有測試使用 **Bun** 運行時和 `bun:test` 框架（NOT Playwright E2E）：

```bash
cd extension
bun test
```

**測試內容**（[authenticator.test.ts](extension/src/background/authenticator.test.ts)）：
- ✅ 算法選擇（支持 ML-DSA-44、-65、-87）
- ✅ 簽名計數單調遞增
- ✅ 認證標記驗證 (UP + UV + AT)
- ✅ RP ID 驗證
- ✅ 算法不支持拋異常
- ✅ Touch ID 隱隐約約 UV 模式回退

---

## 4️⃣ 那個日誌輸出解析

### 日誌內容
```
Skipping user verification: NoopVerifier in use
```

### 原因詳解

**代碼流程：**

1. **[authenticator/__main__.py](authenticator/__main__.py) 啟動**
```python
authenticator = Authenticator(AuthenticatorSettings())
```

2. **[authenticator/service.py#L85-L91](authenticator/service.py#L85-L91) 初始化驗證器**
```python
def __init__(self, ...):
    if sys.platform == "darwin":  # macOS
        self.user_verifier = TouchIDVerifier()
    else:  # 其他平台（Windows/Linux）
        self.user_verifier = NoopVerifier()  # ← 您運行的是 Windows！
```

3. **make_credential 調用時**
```python
def make_credential(self, ...):
    self._verify_user(f"Touch ID to register {options.user.displayName}")
    # 調用 _verify_user → self.user_verifier.verify_user()
```

4. **[authenticator/touch.py#L69-L75](authenticator/touch.py#L69-L75) 執行 NoopVerifier**
```python
class NoopVerifier:
    """User verifier that unconditionally succeeds (useful on non-macOS)."""
    
    def verify_user(self, prompt: str | None = None) -> bool:
        LOGGER.info("Skipping user verification: NoopVerifier in use")
        return True  # ← 無條件返回 True
```

### 為什麼這樣設計？

| 平台 | 驗證器 | 行為 |
|------|-------|------|
| **macOS** | `TouchIDVerifier` | 調用 LocalAuthentication framework（真實指紋驗證） |
| **Windows/Linux** | `NoopVerifier` | 跳過驗證（無硬件支持） |

### ⚠️ 安全含義

- **開發環境**：`NoopVerifier` 允許測試流程而無需指紋認證
- **生產環境**：應該使用平台原生的驗證器（Windows Hello、Linux PAM 等）
- **注意**：`user_verified` 標志仍然設置為 `True` 在認證數據中

```python
auth_data = build_authenticator_data(
    user_verified=True,  # ← 即使 NoopVerifier 也報告為已驗證
    # ...
)
```

---

## 5️⃣ 完整工作流示例

### 場景：用戶在 localhost:3000 註冊

```
┌─────────────────────────────────────────────────────────────────┐
│ 用戶點擊 "Register" 按鈕在 localhost:3000                        │
└──────────────────────┬──────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────────────┐
│ RP Server (Flask) 生成挑戰                                      │
│ POST /register { challenge, user_id, ... }                      │
└──────────────────────┬──────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────────────┐
│ 前端 JavaScript 調用：                                           │
│ navigator.credentials.create({                                  │
│   publicKey: { challenge, rp, user, ... }                       │
│ })                                                              │
└──────────────────────┬──────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────────────┐
│ Playwright 注入的 JavaScript 攔截此調用                          │
│ 轉換 ArrayBuffer → Base64URL                                    │
└──────────────────────┬──────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────────────┐
│ 調用暴露的 Python 綁定：                                         │
│ await window.__pqMakeCredential({                               │
│   publicKey: { challenge: "...", ... }  // Base64URL            │
│ })                                                              │
└──────────────────────┬──────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────────────┐
│ Python authenticator.make_credential() 處理：                    │
│ 1. 驗證 origin/rpId 匹配                                         │
│ 2. 調用 _verify_user()                                          │
│    → NoopVerifier.verify_user()                                 │
│    → 日誌："Skipping user verification: NoopVerifier in use"   │
│ 3. 排除清單檢查                                                  │
│ 4. 生成 ML-DSA-44 密鑰對                                        │
│ 5. 簽署認證數據                                                  │
│ 6. 返回認證器證明對象                                            │
└──────────────────────┬──────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────────────┐
│ JavaScript 轉換返回值：                                          │
│ Base64URL → ArrayBuffer                                         │
└──────────────────────┬──────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────────────┐
│ 前端提交給 RP Server：                                           │
│ POST /register/response { id, type, response: {...} }           │
└──────────────────────┬──────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────────────┐
│ RP Server 驗證認證器證明                                         │
│ ✓ 檢查簽署                                                       │
│ ✓ 檢查算法 (ML-DSA-44)                                          │
│ ✓ 存儲公鑰                                                       │
└─────────────────────────────────────────────────────────────────┘

[日誌輸出]:
Authenticator: Register]: Processing credential creation
{
  "origin": "http://localhost:3000",
  "request_id": "551490bf",
  "user": "alice",
  "user_handle": "cWdWZVh6b25NZzJwbURsM0RmUTNp"
}
Skipping user verification: NoopVerifier in use
[Authenticator: Register]: Credential creation completed
```

---

## 6️⃣ 關鍵算法支持

### 後量子算法
| COSE 算法 ID | 算法名稱 | 優先級 |
|-------------|---------|--------|
| `-48` | ML-DSA-44 | 推薦（最快） |
| `-49` | ML-DSA-65 | 中等 |
| `-50` | ML-DSA-87 | 最安全 |

**選擇邏輯** ([service.py#L235-L240](authenticator/service.py#L235-L240))：
```python
def _select_algorithm(self, pub_key_params: List) -> int:
    # 選擇第一個支持的 PQ 算法
    for param in pub_key_params:
        if param['alg'] in COSE_ALG_TO_OQS:
            return param['alg']
    raise NotSupportedError("No PQ algorithm offered")
```

---

## 7️⃣ 存儲層

### 憑證存儲位置
- **Python**：[authenticator/data/credential_index.json](authenticator/data/credential_index.json)
- **Extension**：Chrome `chrome.storage.local`（加密）

### 存儲的數據
```json
{
  "credential_id": "base64url_encoded_id",
  "user_handle": "base64url_user_id",
  "rp_id": "localhost",
  "algorithm": -48,
  "public_key": "base64url_public_key",
  "private_key": "base64url_private_key",
  "sign_count": 0,
  "created_at": "2026-05-20T12:00:00Z"
}
```

---

## 8️⃣ 測試體系結構

### 現狀
✅ **已實現**：
- [authenticator/tests/](authenticator/tests/) — Python 單元測試
- [extension/src/background/*.test.ts](extension/src/background/) — TypeScript 單元測試（Bun）

❌ **未實現**：
- 端對端 (E2E) Playwright 測試
- 集成測試（RP Server + Authenticator）

### 計劃中的 E2E 測試
根據 [codex/plan.md](codex/plan.md)，E2E 測試應該：
1. 啟動前端 (Next.js)
2. 啟動 RP Server (Flask)
3. 啟動 Playwright Bridge
4. 執行完整的註冊/登入流程
5. 驗證端到端工作

---

## 9️⃣ 調試技巧

### 查看詳細日誌
```bash
# Python 級別
LOGLEVEL=DEBUG python -m authenticator --url http://localhost:3000

# RP Server 級別
export FLASK_ENV=development
python -m rp_server.app
```

### 常見問題

**Q：為什麼看到 "NoopVerifier"？**
A：您在非 macOS 平台運行。這是正常的，允許在開發時跳過生物識別驗證。

**Q：憑證存儲在哪裡？**
A：Python 服務: `authenticator/data/credential_index.json`；Extension: `chrome://extensions/` → Storage

**Q：如何修改支持的算法？**
A：編輯 [authenticator/config.py](authenticator/config.py) 的 `SUPPORTED_ALGORITHMS`

**Q：extension 和 Playwright Bridge 有什麼區別？**
A：
- **Extension**：獨立的瀏覽器擴展，可以從擴展商店安裝
- **Playwright Bridge**：用於本地測試/演示的 Python 實現

---

## 🔟 相關文件參考

| 文件 | 用途 |
|------|------|
| [authenticator/bridge.py](authenticator/bridge.py) | Playwright 集成 |
| [authenticator/service.py](authenticator/service.py) | 核心認證邏輯 |
| [authenticator/touch.py](authenticator/touch.py) | 用戶驗證（Touch ID/Noop） |
| [extension/src/background/authenticator.ts](extension/src/background/authenticator.ts) | Extension 認證器 |
| [rp_server/app.py](rp_server/app.py) | RP Server |
| [codex/SECURITY_REPORTS/](codex/SECURITY_REPORTS/) | 安全分析 |

---

**最後更新**：2026-05-20  
**版本**：1.0 - 完整架構文檔
