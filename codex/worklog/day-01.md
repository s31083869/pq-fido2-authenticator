# Day 1：守則與工具設定 + 前置修正

| 項目 | 內容 |
|---|---|
| 日期 | 2026-11-16 |
| 分支 | `day-01`（從 `origin/main` 83d4f58 開出） |
| 狀態 | 開工完成：理解確認已對上、測試案例已核准，開始實作 |

---

## 開工

### 今日目標

依序完成，每一項各自一個 commit（訊息格式 `Day 1: …`）：

**A. 守則與工具設定**
1. 建立根目錄 `CLAUDE.md`：寫入 11/16 確認的共識總覽
2. 開始使用 `codex/worklog/` 工作紀錄；名詞表以 `codex/PROTOCOL-GUIDE.html` 第 11 章為唯一版本，不另建 `GLOSSARY.md`（11/16 決定）
3. 在 `pyproject.toml` 設定 pytest 的 `testpaths`
4. 用 ruff 統一排版，並移除 1 個未使用的 import（只動排版，不改邏輯）
5. 新增 GitHub Actions CI：`.github/workflows/ci.yml`
6. 新增協議導覽 `codex/PROTOCOL-GUIDE.html`，並在 `README.md` 加上連結（開工時使用者新增的需求：讓自己和之後接手的學弟妹能從零看懂專案）

**B. 前置修正（原本的 Day 1）**

6. RP 驗章改用收到的原始 `clientDataJSON` bytes 計算 hash
7. Python authenticator 的 `allowCredentials` 比對改成符合規格（找不到或 rpId 不符時拒絕）
8. 缺少 `origin` 時給出明確的錯誤，取代不存在的 `self.settings.origin`

**C. 文件**

9. 在 `codex/REPORTS.md` 的 Decision Log 補記 D1–D6 與專案守則
10. 更新 `codex/FN-DSA-PLAN.md`：日期整體順延 2 天（Day 1 = 11/16、Day 12 = 11/27），勾選完成項目

### 架構背景

#### 1. 登入驗章時，RP 要對「原始 bytes」算 hash

WebAuthn 登入（assertion）時，authenticator 簽章的內容是：

```text
authenticatorData ‖ SHA-256(clientDataJSON)
```

`clientDataJSON` 是一串 JSON 文字的 **bytes**，內容包含 `type`、`challenge`、`origin`。RP 驗章時必須對「收到的那串 bytes」算 SHA-256。

目前 RP（`rp_server/services.py:155`，修改前的行號）的作法是：先把 `clientDataJSON` 解析成 Python 物件，再用 `json.dumps` **自己重組一次 JSON**，然後才算 hash。只要 authenticator 產生 JSON 的方式稍有不同（空白、欄位順序、跳脫字元），重組出來的 bytes 就會跟被簽章的 bytes 不一樣，結果合法的簽章也會驗不過。現在之所以沒出事，只是因為兩個 authenticator 剛好都產生緊湊格式、欄位順序也相同的 JSON。

#### 2. `allowCredentials`：只能從 RP 指定的憑證裡挑

登入時，RP 會在 `allowCredentials` 列出「這個使用者有哪些憑證可以用」。依照規格，authenticator 只能從這份清單中挑一把**屬於目前網站（rpId 相符）**的憑證；一把都找不到，就必須回錯誤，不能簽章。

目前 Python authenticator（`authenticator/service.py:269–279`）有兩個問題：
- 清單裡的憑證一把都找不到時，會**改用同網站的任何一把金鑰**簽章。
- 從清單中挑憑證時，**沒有檢查 rpId**，所以可能拿別的網站的金鑰來簽章。

Extension 版的 `pickCredentialForAssertion()` 這兩點都做對了，這次讓 Python 版跟它一致。

#### 3. `origin` 是 `clientDataJSON` 的必要欄位

authenticator 必須知道頁面的 origin，才能寫出 `clientDataJSON`。`make_credential()`、`get_assertion()` 在沒有傳入 origin 時，會去讀 `self.settings.origin`（`authenticator/service.py:108`、`:190`），但設定類別裡**根本沒有這個欄位**，結果會丟出看不懂的 `AttributeError`。這次改成直接回報「缺少 origin」。

#### 4. 設定類工作的原因

- **`testpaths`**：在根目錄直接跑 `pytest` 時，會掃到並執行 `extension/emsdk` 裡第三方套件的範例程式（11/13 曾因此在根目錄產生 `test_localsystem.txt`）。設定 `testpaths` 後，pytest 只會找我們自己的測試。
- **ruff 排版**：有 11 個檔案沒有照統一格式排版。先單獨 commit 一次排版，之後每天的 diff 才只會出現真正的修改。
- **CI**：每次開 PR，GitHub 都會在一台乾淨的 Linux 機器上重跑全部檢查，提供一個「不是 Claude」的獨立結果。

### 預計修改

| 檔案 | 預計修改 | 對應項目 |
|---|---|---|
| `CLAUDE.md`（新增） | 專案守則 | A1 |
| `pyproject.toml` | 新增 `[tool.pytest.ini_options]` 的 `testpaths` | A3 |
| `authenticator/` 8 個檔案、`rp_server/` 3 個檔案 | ruff 排版（`bridge.py`、`config.py`、`service.py`、`storage.py`、`touch.py`、`webauthn.py`、`tests/conftest.py`、`tests/test_authenticator.py`、`app.py`、`database.py`、`services.py`） | A4 |
| `rp_server/models.py` | 移除未使用的 `Column` import | A4 |
| `.github/workflows/ci.yml`（新增） | CI 流程 | A5 |
| `codex/PROTOCOL-GUIDE.html`（新增） | 協議導覽：流程圖、資料結構、演算法、程式碼地圖、名詞表 | A6 |
| `README.md` | 加上協議導覽的連結 | A6 |
| `rp_server/services.py` | `verify_authentication_payload()` 改用原始 bytes 計算 hash | B6 |
| `rp_server/tests/` | 新增驗章測試 T1、T2 | B6 |
| `authenticator/service.py` | `_locate_credential()` 比對規則；`make_credential()`、`get_assertion()` 的 origin 檢查 | B7、B8 |
| `authenticator/tests/test_authenticator.py` | 新增測試 T3–T6 | B7、B8 |
| `codex/REPORTS.md` | Decision Log 新增 D1–D6 與守則 | C9 |
| `codex/FN-DSA-PLAN.md` | 日期順延、勾選 | C10 |

### 測試案例（待你核准）

| 編號 | 情境 | 預期結果 | 依據 | 實作前預期 |
|---|---|---|---|---|
| T1 | authenticator 送出的 `clientDataJSON` 格式合法，但含有空白、欄位順序也不同；簽章是對這串原始 bytes 計算的（用真的 liboqs ML-DSA-44） | `/authenticate/verify` 回傳成功 | WebAuthn §7.2：RP 對收到的 `clientDataJSON` 原始 bytes 計算 SHA-256 | 紅燈（RP 重組 JSON 後 hash 不同） |
| T2 | 簽章完成後，把 `clientDataJSON` 裡 RP 不會檢查的 `crossOrigin` 從 `false` 改成 `true` | 回傳 400「Invalid signature」 | WebAuthn §7.2：簽章涵蓋 `clientDataJSON` 的 hash，任何竄改都必須讓驗章失敗 | 綠燈（回歸保護：確認修正沒有削弱安全性） |
| T3 | authenticator 存有 example.com 的憑證 A；`allowCredentials` 只列出不存在的憑證 B | 拋出 `CredentialStoreError`，不產生簽章 | Phase-1 spec 6.2：清單內一把都找不到時必須中止；WebAuthn §6.3.3 | 紅燈（目前會改用 A 簽章） |
| T4 | authenticator 存有 other.com 的憑證 C；登入 example.com 時，`allowCredentials` 列出 C | 拋出 `CredentialStoreError` | Phase-1 spec 6.2：必須「在清單中」**而且**「rpId 相符」 | 紅燈（目前不檢查 rpId） |
| T5 | `allowCredentials` 為空，authenticator 存有 example.com 的憑證 | 成功簽章，使用該憑證 | Phase-1 spec 6.2：清單為空時，依 rpId 選第一把 | 綠燈（回歸保護） |
| T6 | 呼叫 `make_credential()`、`get_assertion()` 時沒有提供 origin | 拋出 `ValueError`，訊息指出缺少 origin | WebAuthn §5.8.1：origin 是 `clientDataJSON` 的必要欄位 | 紅燈（目前丟出 `AttributeError`） |

**破壞檢查**：T1 和 T3、T4 是今天的關鍵測試。實作完成後，我會把實作暫時改回舊行為，確認這三個測試確實會變紅，再改回來。

### 設定類工作的驗收方式（不寫單元測試）

| 編號 | 驗收方式 |
|---|---|
| S1 | 在根目錄直接執行 `pytest`：只收集 `authenticator/tests`、`rp_server/tests`，而且根目錄沒有新增任何檔案 |
| S2 | `ruff check`、`ruff format --check` 全部通過；排版前後的測試結果相同（證明只動了排版） |
| S3 | PR 上的 CI 全部是綠勾 |
| S4 | 你審閱 `CLAUDE.md`，確認內容和共識總覽一致 |

### 對齊紀錄

- 介紹今日內容：三個修正與設定工作。使用者要求先提供一份能從零理解協議的導覽，已完成（A6）。
- 決定：名詞表以協議導覽第 11 章為唯一版本，不另建 `GLOSSARY.md`。
- 理解確認問答：
  - 問題 1（原始 bytes 的 hash）：使用者指出 RP 驗的是重組後的版本，多一個空格內容就不同。Claude 補充完整的因果：bytes 不同 → SHA-256 不同 → 合法簽章驗章失敗。已對上。
  - 問題 3（origin）：使用者指出自動填預設值就無法防範跨域攻擊。Claude 補充：釣魚網站的請求會被當成來自正牌網站，RP 的 origin 檢查與 authenticator 的 rpId／origin 檢查都會失效。已對上。
  - 問題 2（allowCredentials）：使用者請 Claude 先解釋「清單」是什麼。Claude 用 alice／alice1 的例子說明，並依使用者要求把例子補進協議導覽第 5 章。使用者回答「一把都找不到就不可能驗證成功」。Claude 補充：找不到不代表帳號沒有註冊（RP 只在帳號有憑證時才回傳清單），而是這台 authenticator 沒有該帳號的鑰匙，此時必須主動回報錯誤，不能改用其他鑰匙。已對上。
- 測試案例 T1–T6：使用者已於 11/16 核准。

### 執行順序說明

ruff 排版（A4）排在開工文件之後的第一個 commit。現有程式有 1 個 lint 錯誤、11 個檔案未排版，先處理掉，之後每個 commit 才能都通過 `ruff check` 與 `ruff format --check`。開工文件的 commit 只含文件，當下 ruff 仍未通過，這是既有問題，不是本次修改造成的。

---

## 完工

（完成後補上：實際修改的檔案與行號、測試結果、破壞檢查、獨立審查、待辦清單）
