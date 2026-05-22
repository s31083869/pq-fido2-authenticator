
## 🏁 Project Overview

### 目標與範圍 (Goal & Scope)
本專案旨在建立一個 **Post-Quantum FIDO2 Authenticator (Software-based)**，  
使用 **Python 環境** 作為軟體 authenticator，  
並確保可完成 [Yubico WebAuthn Demo](https://demo.yubico.com/webauthn-developers) 的註冊與登入流程。  

此實作屬於 **Proof-of-Concept (PoC)** 性質，著重於驗證 PQC (Post-Quantum Cryptography) 在 FIDO2 流程中的可行性與整合性。  

### 設計邊界 (Assumptions & Boundaries)
- Authenticator 為軟體模擬（非硬體安全模組），主要執行於 macOS。
- 可攔截 `navigator.credentials.create()` / `get()` 流程，將 WebAuthn JS 互動導入 Python 處理。
- RP Server 與 Frontend 均為自行開發，可接受自定 JSON/Base64 結構（非強制 CBOR/COSE）。
- 若未來需對接標準 RP，可於 RP 層新增格式轉換器。

---

## 🧩 System Architecture

### 架構概覽
```text
Frontend (Next.js)
  ↕ (navigator.credentials.create / get)
RP Server (Flask)
  ↕ (HTTP JSON)
Python Authenticator (黑盒)
  ├─ Playwright → Chromium (JS interception)
  ├─ Touch ID → pyobjc
  ├─ PQC KeyGen → liboqs-python
  └─ Credential Storage → keyring (macOS Keychain)
```

### 模組關係
- **Frontend**：發起 FIDO2 註冊與登入請求，處理使用者互動。
- **RP Server (Flask)**：產生 challenge，驗證 Authenticator 回傳的資料結構與簽章。
- **Authenticator (Python)**：作為黑盒執行 WebAuthn API 攔截與模擬，提供 Touch ID 驗證與 PQC keypair 生成。

---

## 🧠 Components

### Authenticator
- 全部在 Python 環境內執行。
- 使用：
  - `playwright`：啟動 Chromium 攔截 WebAuthn JS API。
  - `pyobjc`：呼叫 macOS Touch ID 作為使用者驗證 (UV)。
  - `liboqs-python`：產生後量子簽章演算法金鑰。
    - 支援演算法：
      - ML-DSA-44 (`alg: -48`)
      - ML-DSA-65 (`alg: -49`) — 預設
      - ML-DSA-87 (`alg: -50`)
  - `keyring`：將憑證儲存在 macOS Keychain。

#### Authenticator API 設計（建議）
```python
class Authenticator:
    def make_credential(self, options: PublicKeyCredentialCreationOptions) -> dict:
        """模擬 navigator.credentials.create()"""
        ...

    def get_assertion(self, options: PublicKeyCredentialRequestOptions) -> dict:
        """模擬 navigator.credentials.get()"""
        ...

class UserVerifier:
    def verify_user(self) -> bool:
        """呼叫 Touch ID 驗證"""
        ...
```

---

### RP Server
- 使用 **Flask** + **SQLAlchemy** + **liboqs-python**。
- 已安裝套件：`flask`, `flask-cors`, `pydantic`, `pydantic-settings`, `sqlalchemy`, `liboqs-python`。
- 提供以下 API：
  - `POST /register/options`：產生註冊挑戰。
  - `POST /register/verify`：驗證 attestation。
  - `POST /authenticate/options`：產生登入挑戰。
  - `POST /authenticate/verify`：驗證 assertion。

#### 資料庫結構（範例）
```python
class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    display_name = Column(String)

class Credential(Base):
    __tablename__ = "credential"
    id = Column(String, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    public_key = Column(Text)
    algorithm = Column(Integer)
    sign_count = Column(Integer)
```

---

### Frontend
- 基於 **Next.js** + **bun**。
- 已安裝：
  - `react-hook-form`
  - `zod`
  - `@hookform/resolvers`
  - 所有 Shadcn UI 組件。
- 使用 `navigator.credentials` 完成註冊與登入流程。
- 以 `zod` Schema 驗證從 RP Server 傳入的 JSON。

#### Example Zod Schema
```ts
const RegisterOptionsSchema = z.object({
  challenge: z.string(),
  rp: z.object({ id: z.string(), name: z.string() }),
  user: z.object({ id: z.string(), name: z.string(), displayName: z.string() }),
  pubKeyCredParams: z.array(z.object({ type: z.literal("public-key"), alg: z.number() })),
});
```

---

## 🧱 Rules

### Global
- 遵循 `DRY` 原則與 `TDD` 測試導向。
- 需善用設計模式，可參考：
  - `codex/design-patterns/python.md`
  - `codex/design-patterns/typescript.md`

### Python
- 套件與指令管理：`uv`
- 型別檢查：`pyright`
- 程式風格：`ruff`
- 單元測試：`pytest`

### TypeScript
- 套件管理：`bun`
- 檔名命名：`kebab-case`
- 測試框架：`bun:test`

---

## 🧾 Note

可參考：
- `codex/docs/cdp-webauthn-interface.md` → Chromium CDP WebAuthn Emulator 介面。
- `codex/docs/liboqs-python.md` → liboqs API。
- `codex/docs/python-fido2.md` → python-fido2 API。

---

## 🧩 Example Data Structures

### 🔐 Registration (Create)
```json
{
  "publicKey": {
    "attestation": "none",
    "authenticatorSelection": {
      "requireResidentKey": false,
      "residentKey": "discouraged",
      "userVerification": "preferred"
    },
    "challenge": "RsUBGZNfckMhB+ZizQ2APQ==",
    "excludeCredentials": [],
    "pubKeyCredParams": [
      { "alg": -48, "type": "public-key" },
      { "alg": -49, "type": "public-key" },
      { "alg": -50, "type": "public-key" }
    ],
    "rp": { "id": "demo.yubico.com", "name": "Yubico Demo" },
    "timeout": 90000,
    "user": {
      "displayName": "Alice",
      "id": "Base64UserId",
      "name": "alice"
    }
  }
}
```

**Authenticator Response**
- 由 Python Authenticator 生成（JSON / Base64 編碼）
- 主要欄位：
  - `clientDataJSON`
  - `attestationObject`
  - `publicKeyAlgorithm`
  - `publicKey`
  - `id` / `rawId`

---

### 🔑 Authentication (Get)
```json
{
  "publicKey": {
    "allowCredentials": [{ "id": "Base64CredentialId", "type": "public-key" }],
    "challenge": "4jcPW3G1iT1k3MhO/0kaZw==",
    "rpId": "demo.yubico.com",
    "timeout": 90000,
    "userVerification": "preferred"
  }
}
```

**Authenticator Response**
- 由 Python Authenticator 生成。
- 主要欄位：
  - `authenticatorData`
  - `clientDataJSON`
  - `signature`
  - `userHandle`

---

## 🧪 Development & Testing

### 開發環境啟動
| 模組 | 指令範例 |
|------|-----------|
| Frontend | `bun dev` |
| RP Server | `uv run flask run` |
| Authenticator | `python -m authenticator --url <target>` |

### 測試方式
- **Unit Test**：使用 `pytest` / `bun:test`
- **E2E Test**：使用 Playwright 自動執行完整 WebAuthn 註冊與登入流程
- **CI/CD**：在 pipeline 中整合 type-check 與測試

---

## ⚙️ Workflow

1. Developer 撰寫 / 更新 `spec.md`
2. Agent 生成 `plan.md`（clarify / plan / risk / interface）
3. Developer 審閱並確認 `plan.md`
4. 進入實作與測試階段
