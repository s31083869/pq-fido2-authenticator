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

> **更正（11/16，依獨立審查）**：上面提到「欄位順序」並不正確。Python 的 `json.loads` 再 `json.dumps` 會保留欄位順序，所以只換順序的緊湊 JSON，在舊版 RP 也能驗過。重組後真正會不同的是空白、跳脫字元的寫法與重複欄位。T1 變紅的原因是空白，測試本身仍然有效。

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

### 追加工作（11/16，依獨立審查，使用者決定當天修正）

獨立審查發現兩個 Day 1 之前就存在的安全問題，使用者決定今天一併修正。

#### 1. credential ID 必須完全相同才算同一張憑證

Windows 上的儲存層把 credential ID 直接接成檔名 `<ID>.bin`（`authenticator/storage.py:146`），讀出檔案後也沒有確認裡面的 ID 是否就是要找的那一個（`storage.py:110–117`）。造成兩個問題：
- Windows 的檔案系統不分大小寫，大小寫互換的 ID 會開到同一個檔案。
- 含有路徑的 ID（例如 `../credentials/<ID>`）也會解析到同一個檔案。

結果是 RP 清單裡明明沒有某把憑證，authenticator 卻可能選中它；`excludeCredentials` 也可能因此誤判成重複註冊。rpId 檢查仍然有效，所以不會被拿去登入其他網站。

修正方式：
- 儲存層只接受由 base64url 字元（A–Z、a–z、0–9、`-`、`_`）組成的 ID，其他一律當作找不到。
- 讀出檔案後，比對裡面的 ID 是否和要找的完全相同。

#### 2. origin 必須取自頁面實際的網址

Python bridge 直接使用頁面傳來的 `payload["origin"]`（`authenticator/bridge.py:223`、`:231`），頁面可以任意偽造。真正的瀏覽器裡，origin 是由瀏覽器依照呼叫者的真實來源填入，網頁無法指定。Playwright 呼叫 binding 時附帶的 `source["frame"].url` 就是呼叫者頁面的真實網址。

修正方式：bridge 改從 `source["frame"].url` 取出「協定＋網域＋埠」當作 origin，不再採用頁面自稱的值。

#### 追加的預計修改

| 檔案 | 預計修改 |
|---|---|
| `authenticator/storage.py` | `_credential_file()` 檢查 ID 字元；`load()` 比對讀出的 ID 是否完全相同 |
| `authenticator/bridge.py` | `_handle_make()`、`_handle_get()` 改用 `source["frame"].url` 推出 origin |
| `authenticator/tests/test_authenticator.py` | 新增 T7–T9 |
| `authenticator/tests/test_bridge.py`（新增） | 新增 T10、T11 |

#### 追加的測試案例（待你核准）

| 編號 | 情境 | 預期結果 | 依據 | 實作前預期 |
|---|---|---|---|---|
| T7 | authenticator 存有憑證 A；`allowCredentials` 列出的 ID 和 A 只差在大小寫 | 拒絕：拋出 `CredentialStoreError`（No credential available） | credential ID 是不透明的 bytes，必須完全相同才算同一張憑證（WebAuthn §6.3.3 依 ID 查找；Phase-1 spec 6.2） | Windows 上紅燈（會選中 A） |
| T8 | `allowCredentials` 列出含路徑的 ID：`../credentials/<A 的 ID>` | 拒絕：拋出 `CredentialStoreError`（No credential available） | 同上；ID 不能被當成路徑解讀 | Windows 上紅燈（會選中 A） |
| T9 | authenticator 存有憑證 A；註冊時 `excludeCredentials` 列出和 A 只差大小寫的 ID | 不視為重複註冊，註冊成功 | WebAuthn §6.3.2 authenticatorMakeCredential：依 ID 查找 excludeCredentials，必須完全相同 | Windows 上紅燈（誤判為重複而拒絕） |
| T10 | 頁面在 payload 中自稱 origin 是 `http://localhost:3000`，但呼叫 binding 的頁面實際網址是 `https://evil.example/login` | bridge 交給 authenticator 的 origin 是 `https://evil.example`（註冊、登入兩個入口都要） | WebAuthn §5.8.1：origin 由瀏覽器依呼叫者真實來源填入，網頁無法指定；bridge 扮演瀏覽器的角色 | 紅燈（目前直接採用頁面自稱的值） |
| T11 | payload 中沒有 origin，頁面實際網址是 `http://localhost:3000/register?step=2` | origin 只取協定、網域、埠：`http://localhost:3000` | origin 的定義（協定＋網域＋埠） | 紅燈（目前會變成沒有 origin） |

注意：T7–T9 的問題來自 Windows 檔案系統不分大小寫。CI 在 Linux 上改用 keyring 儲存，這三個測試在修正前後都會是綠燈，在 Linux 上的作用是回歸保護；紅燈只會在 Windows 上出現。

**破壞檢查**：T7、T9 拿掉「ID 完全相同」的比對；T8 拿掉 ID 字元檢查並同時拿掉比對；T10 改回採用頁面自稱的 origin。

#### 追加工作的對齊紀錄

- 問題 A（為什麼大小寫互換的 ID 會選到原本的憑證）：使用者回答「Windows 不分大小寫」。Claude 補充：精確地說，是 Windows 的檔案系統比對檔名時不分大小寫，而 ID 被拿來當檔名；修正的關鍵是讀出後比對檔案內記錄的 ID。已對上。
- 問題 B（為什麼 origin 要取自頁面實際網址）：使用者回答「看 payload 就讓頁面自己說了算」，並請 Claude 詳細說明實作差異。Claude 說明 payload 由頁面填寫、`source` 由 Playwright 填寫，並以 evil.example 偽造 origin 的攻擊流程比較修正前後。確認問題「修正後 evil.example 謊稱 localhost:3000 會怎樣」，使用者回答「拿到 evil.example，和 rpId 不符直接拒絕」。已對上。
- 測試案例 T7–T11：使用者已於 11/16 核准。

### 執行順序說明

ruff 排版（A4）排在開工文件之後的第一個 commit。現有程式有 1 個 lint 錯誤、11 個檔案未排版，先處理掉，之後每個 commit 才能都通過 `ruff check` 與 `ruff format --check`。開工文件的 commit 只含文件，當下 ruff 仍未通過，這是既有問題，不是本次修改造成的。

---

## 完工

### 實際修改

行號以 Day 1 最後一個 commit 的版本為準。

| commit | 檔案:行號 | 改了什麼 | 目的 |
|---|---|---|---|
| `3ba07d6` | `codex/worklog/day-01.md` | 新增本文件的開工段落 | 在實作前留下測試案例與對齊紀錄 |
| `a1d9134` | `authenticator/` 8 個檔案、`rp_server/` 3 個檔案 | ruff 排版 | 統一格式。排版前後這 11 個檔案的 Python 語法樹（AST）完全相同，證明沒有改到邏輯 |
| `a1d9134` | `rp_server/models.py:5` | 移除未使用的 `Column` import | 修正唯一的 lint 錯誤 |
| `560d865` | `pyproject.toml:29–32` | 新增 `[tool.pytest.ini_options]`，`testpaths` 只含 `authenticator/tests`、`rp_server/tests` | 避免 pytest 掃進並執行 `extension/emsdk` 的第三方程式 |
| `abe91bc` | `CLAUDE.md:1–112`（新增） | 專案守則 | 寫入 11/16 確認的共識，Claude 每次對話都會自動遵守 |
| `3edd6ef` | `codex/PROTOCOL-GUIDE.html:1–1377`（新增）、`README.md:3` | 協議導覽與 README 連結 | 讓新成員從零理解專案；名詞表以導覽第 11 章為唯一版本 |
| `7b1d05c` | `.github/workflows/ci.yml:1–105`（新增） | Python、Extension、Frontend 三個 CI 工作 | PR 時在乾淨的 Linux 機器上重跑必跑檢查；liboqs 0.14.0 依版本快取 |
| `e0b9cb0` | `rp_server/services.py:130–191`（關鍵在第 177 行） | `verify_authentication_payload()` 改用收到的 clientDataJSON 原始 bytes 計算 SHA-256，並補齊整個函式的註解 | 符合 WebAuthn §7.2：合法簽章不會再因 JSON 格式不同而被拒絕 |
| `e0b9cb0` | `rp_server/tests/test_authentication_verify.py:1–139`（新增） | T1（第 94 行）、T2（第 117 行），使用真的 liboqs ML-DSA-44 | 驗證 B6 |
| `6f2b842` | `authenticator/service.py:329–357` | `_locate_credential()` 只從 allowCredentials 中挑選屬於目前 rpId 的憑證，挑不到就回傳 None | 符合 Phase-1 spec 6.2 |
| `6f2b842` | `authenticator/storage.py:10`，以及原第 139–147 行 | 移除不再使用的 `find_first()` 與 `Iterable` import | 不留下沒有用到的程式 |
| `6f2b842` | `authenticator/tests/test_authenticator.py:159–207` | T3（第 159 行）、T4（第 173 行）、T5（第 191 行） | 驗證 B7 |
| `95854cb` | `authenticator/service.py:370–381` | 新增 `_require_origin()`：缺少 origin 時丟出 `ValueError` | 取代不存在的 `self.settings.origin` |
| `95854cb` | `authenticator/service.py:107–216`、`219–312` | `make_credential()`、`get_assertion()` 改用 `_require_origin()`，並補齊整個函式的註解 | 同上，並依守則補註解 |
| `95854cb` | `authenticator/tests/test_authenticator.py:209–224` | T6（兩種情況） | 驗證 B8 |
| `e3f4f38` | `codex/REPORTS.md:381–400` | Decision Log 第 40–53 號 | 記錄標準查證結論、D1–D6、守則與三個修正 |
| 完工紀錄 | `codex/FN-DSA-PLAN.md` | 日期順延 2 天、勾選 Day 1、每日流程與分支規則改為指向 `CLAUDE.md` | 讓計畫和實際進度一致 |
| 完工紀錄 | `codex/worklog/day-01.md` | 完工段落 | 本段 |

### 測試結果（實作前 → 實作後）

| 測試 | 實作前 | 實作後 |
|---|---|---|
| T1 | 紅燈：RP 回傳 400 `Invalid signature` | 綠燈 |
| T2 | 綠燈（回歸保護） | 綠燈 |
| T3 | 紅燈：`DID NOT RAISE CredentialStoreError`（改拿其他憑證簽章） | 綠燈 |
| T4 | 紅燈：`DID NOT RAISE CredentialStoreError`（使用 other.com 的憑證） | 綠燈 |
| T5 | 綠燈（回歸保護） | 綠燈 |
| T6 | 紅燈：`AttributeError: 'AuthenticatorSettings' object has no attribute 'origin'` | 綠燈 |

整體：Python 測試從 14 個增為 21 個，Extension 11 個、Frontend 4 個，全部通過。從第 2 個 commit 起，每個 commit 都通過 8 項必跑檢查。

### 破壞檢查

| 測試 | 怎麼改壞 | 結果 |
|---|---|---|
| T1 | 驗章改回「解析後重新序列化」再算 hash | T1 變紅 |
| T4 | 拿掉 rpId 的檢查 | 只有 T4 變紅 |
| T3 | 恢復「清單裡找不到就改用同網站第一把」 | 只有 T3 變紅 |

每次檢查後都已改回正確的實作。

### 設定類工作的驗收

| 編號 | 結果 |
|---|---|
| S1 | 通過：在根目錄直接執行 `pytest`，只收集 4 個測試檔（當時共 14 個測試），根目錄沒有新增檔案 |
| S2 | 通過：`ruff check`、`ruff format --check` 都通過；排版前後 11 個檔案的 AST 相同，`models.py` 只少了一個 import |
| S3 | 待 PR 建立後確認 CI 結果 |
| S4 | 通過：使用者於 11/16 審閱 `CLAUDE.md`，確認內容和共識一致 |

### 獨立審查

**第 1 次（T1–T6）**：由沒看過實作過程的子代理審查。它從 git 載入修改前的程式，在記憶體中逐一還原各項修正重跑測試，結果和本文件記錄的破壞檢查一致，全套 21 個測試通過。

| 審查意見 | 分類 | 處理 |
|---|---|---|
| T6 的斷言 `match="origin"` 太弱：`_origin_host()` 的「Invalid origin」也會符合，拿掉修正後 T6 仍會通過 | 必須修正 | 改為 `match="^Missing origin"`（使用者同意），並補做破壞檢查：拿掉 origin 檢查時 T6 變紅。commit `c679adf` |
| 註解與文件說「欄位順序不同」會讓 bytes 不同，這是錯的：`json.loads`／`json.dumps` 會保留順序 | 必須修正 | 更正 `services.py`、測試檔、協議導覽；開工段落加註更正。commit `c679adf` |
| T3、T4 應鎖定拒絕原因 | 建議 | 加上 `match="No credential available"`（使用者同意）。commit `c679adf` |
| `service.py` 一處註解沒有涵蓋清單為空的情況 | 建議 | 已修正。commit `c679adf` |
| credential ID 被當成檔名；bridge 的 origin 可被頁面偽造（皆為 Day 1 之前就存在的問題） | 建議 | 使用者決定當天修正，見開工段落的「追加工作」 |

**第 2 次（T7–T11）**：待追加工作完成後進行。

### 待辦清單（中途發現、今天不處理）

- RP 尚未檢查 signCount 是否遞增（WebAuthn §7.2），也沒有檢查 authenticatorData 的 UP／UV flags。
- Python authenticator 在挑選憑證之前就先要求使用者驗證：找不到憑證時，使用者會先看到 Windows Hello 視窗才收到錯誤。Extension 是先挑憑證再驗證，之後可以考慮讓兩邊一致。
- 新增 `tests/` 資料夾時，要同步加進 `pyproject.toml` 的 `testpaths`、`CLAUDE.md` 與 CI 的 ruff 路徑。
- 前端 eslint 提示 baseline-browser-mapping 的資料過舊；升級依賴要先徵得使用者同意。
- RP 的 CORS 設定允許任何網站呼叫 API（`rp_server/app.py` 的 `CORS(app)` 預設允許所有來源），惡意網站可以替任何帳號索取登入題目。
