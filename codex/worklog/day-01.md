# Day 1：守則與工具設定 + 前置修正

| 項目 | 內容 |
|---|---|
| 日期 | 2026-11-16 |
| 分支 | `day-01`（從 `origin/main` 83d4f58 開出） |
| 狀態 | 完工：A1–A6、B6–B8、C9–C10 與兩次追加工作都已完成，待 PR 的 CI 結果（S3） |

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

> **更正（11/16，依第 2 次獨立審查）**：上面說 T7–T9 的問題都來自 Windows 檔案系統不分大小寫，這對 T8 不正確。T8 的問題是 ID 被當成路徑解讀，和大小寫無關；它在 Linux 上不會變紅，是因為 Linux 用 keyring 儲存，根本不會組出檔案路徑。

**破壞檢查**：T7、T9 拿掉「ID 完全相同」的比對；T8 拿掉 ID 字元檢查並同時拿掉比對；T10 改回採用頁面自稱的 origin。

#### 追加工作的對齊紀錄

- 問題 A（為什麼大小寫互換的 ID 會選到原本的憑證）：使用者回答「Windows 不分大小寫」。Claude 補充：精確地說，是 Windows 的檔案系統比對檔名時不分大小寫，而 ID 被拿來當檔名；修正的關鍵是讀出後比對檔案內記錄的 ID。已對上。
- 問題 B（為什麼 origin 要取自頁面實際網址）：使用者回答「看 payload 就讓頁面自己說了算」，並請 Claude 詳細說明實作差異。Claude 說明 payload 由頁面填寫、`source` 由 Playwright 填寫，並以 evil.example 偽造 origin 的攻擊流程比較修正前後。確認問題「修正後 evil.example 謊稱 localhost:3000 會怎樣」，使用者回答「拿到 evil.example，和 rpId 不符直接拒絕」。已對上。
- 測試案例 T7–T11：使用者已於 11/16 核准。

### 追加工作 2（11/16，依第 2 次獨立審查）

第 2 次獨立審查確認 T7–T11 都有效，但指出兩項安全修正各有一個缺口：程式是對的，只是沒有測試保護，之後重構時被拿掉也不會被發現。

1. **字元檢查沒有測試保護。** 只拿掉 `_credential_file()` 的字元檢查時，28 個測試全部通過，因為 T8 會被 `load()` 讀出後的 ID 比對擋下。但這個比對發生在讀檔、解密之後，那時 authenticator 已經碰過憑證資料夾以外的檔案。在 Windows 上，光是查詢 `//主機/共用資料夾` 這類網路路徑的檔案是否存在，就可能連線到外部主機。
2. **CI 抓不到大小寫問題。** CI 在 Linux 上用 keyring 儲存，測試用的假 keyring 區分大小寫。所以拿掉 `load()` 的 ID 比對時，T7、T9 在 CI 上仍然通過，只有在 Windows 本機跑才會變紅。

兩個新測試都放在 `authenticator/tests/test_storage.py`，在 Linux 與 Windows 上都能偵測到破壞。因為實作已經存在，新測試一寫好就會是綠燈，證明它們有效的是破壞檢查。

#### 追加的測試案例 2（待你核准）

| 編號 | 情境 | 預期結果 | 依據 | 實作前預期 |
|---|---|---|---|---|
| T12 | file 儲存後端；要讀取的 ID 是路徑寫法：`../outside`、`..\outside`、絕對路徑 `<暫存資料夾>/outside` | 回報找不到（`CredentialStoreError`，訊息含 `not found`），而且回報之前完全沒有查詢或讀取任何檔案。測試會把「查詢檔案是否存在」和「讀檔」換成一被呼叫就失敗的版本 | ID 只是識別碼，不能被當成路徑解讀（同 T8）；檢查必須在碰到檔案系統之前完成 | 綠燈（字元檢查已在 `2192982` 加上）。破壞檢查：只拿掉字元檢查時必須變紅 |
| T13 | keyring 儲存後端，但比對名稱時不分大小寫（模擬 Windows，讓 Linux 的 CI 也能重現）；已存憑證 A；要讀取的 ID 和 A 只差大小寫 | 回報找不到（`CredentialStoreError`，訊息含 `not found`）；用 A 原本的 ID 讀取時正常取得 A | 同 T7：credential ID 必須完全相同才算同一張憑證（WebAuthn §6.3.3；Phase-1 spec 6.2） | 綠燈（ID 比對已在 `2192982` 加上）。破壞檢查：只拿掉 ID 比對時必須變紅 |

注意：`..\outside` 只有在 Windows 上才會被解讀成路徑；在 Linux 上它只是含有反斜線的檔名，同樣會被字元檢查擋下。

**破壞檢查**：T12 只拿掉字元檢查；T13 只拿掉 `load()` 的 ID 比對。

#### 待你決定：注入腳本裡用不到的 origin

注入腳本仍在 payload 放 `origin: window.location.origin`（`bridge.py:140`、`:152`），但 bridge 已經不使用它。讀者看注入腳本時，可能會以為 origin 是從這裡來的。

#### 追加工作 2 的對齊紀錄

- 問題 C（`load()` 讀出後已經會比對 ID，為什麼讀檔之前還要檢查字元）：使用者一開始請 Claude 再解釋。Claude 把 `load()` 拆成 5 步說明（組路徑 → 查檔案是否存在 → 讀檔 → 解密 → 比對 ID），比對在第 5 步，字元檢查在第 1 步。使用者回答「不然 1–4 步都做了才發現不一樣，中間做了很多無謂且不安全的事情」。已對上。
- 問題 D（為什麼 T7、T9 在 CI 上抓不到「拿掉 ID 比對」）：Claude 說明 Windows 的檔名不分大小寫，所以大小寫互換的 ID 會開到憑證 A；CI 的假 keyring 區分大小寫，所以根本查不到 A，有沒有比對都會回報找不到。使用者表示理解。
- 測試案例 T12、T13：使用者已於 11/16 核准。
- 注入腳本的 origin：使用者選擇刪掉這兩行，並補齊 `wrapNavigator()` 的註解。這不改變行為，所以沒有新的測試案例。
- 測試範圍（使用者決定，只適用於今天剩下的 commit）：破壞檢查只做 T12、T13。commit 前不再跑全套 pytest 與 bun 檢查，只跑新測試與 ruff；全套由 PR 上的 CI 執行。`CLAUDE.md` 的通用規則不變。

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
| `e0b9cb0` | `rp_server/services.py:130–192`（關鍵在第 178 行） | `verify_authentication_payload()` 改用收到的 clientDataJSON 原始 bytes 計算 SHA-256，並補齊整個函式的註解 | 符合 WebAuthn §7.2：合法簽章不會再因 JSON 格式不同而被拒絕 |
| `e0b9cb0` | `rp_server/tests/test_authentication_verify.py:1–140`（新增） | T1（第 94 行）、T2（第 118 行），使用真的 liboqs ML-DSA-44 | 驗證 B6 |
| `6f2b842` | `authenticator/service.py:329–357` | `_locate_credential()` 只從 allowCredentials 中挑選屬於目前 rpId 的憑證，挑不到就回傳 None | 符合 Phase-1 spec 6.2 |
| `6f2b842` | `authenticator/storage.py:10`，以及原第 139–147 行 | 移除不再使用的 `find_first()` 與 `Iterable` import | 不留下沒有用到的程式 |
| `6f2b842` | `authenticator/tests/test_authenticator.py:159–207` | T3（第 159 行）、T4（第 174 行）、T5（第 192 行） | 驗證 B7 |
| `95854cb` | `authenticator/service.py:370–381` | 新增 `_require_origin()`：缺少 origin 時丟出 `ValueError` | 取代不存在的 `self.settings.origin` |
| `95854cb` | `authenticator/service.py:107–216`、`219–312` | `make_credential()`、`get_assertion()` 改用 `_require_origin()`，並補齊整個函式的註解 | 同上，並依守則補註解 |
| `95854cb` | `authenticator/tests/test_authenticator.py:210–225` | T6（兩種情況） | 驗證 B8 |
| `e3f4f38` | `codex/REPORTS.md:381–400` | Decision Log 第 40–53 號 | 記錄標準查證結論、D1–D6、守則與三個修正 |
| `c679adf` | `authenticator/tests/test_authenticator.py:170`、`188`、`223–224` | T3、T4 加上 `match="No credential available"`；T6 改為 `match="^Missing origin"` | 依第 1 次獨立審查鎖定拒絕原因，避免其他錯誤讓測試誤判通過 |
| `c679adf` | `rp_server/services.py:175–177`、`rp_server/tests/test_authentication_verify.py:95–99`、`codex/PROTOCOL-GUIDE.html:769`、本文件第 50 行 | 更正「欄位順序不同會讓 bytes 不同」的錯誤敘述 | 依第 1 次獨立審查 |
| `c679adf` | `authenticator/service.py:250` | 註解補上清單為空的情況 | 依第 1 次獨立審查 |
| `c0e3000` | `codex/worklog/day-01.md:122–171` | 開工段落新增「追加工作」：兩個安全問題、預計修改、T7–T11 與對齊紀錄 | 在實作前留下追加的測試案例與核准紀錄 |
| `2192982` | `authenticator/storage.py:7`、`18–20` | 新增 `_CREDENTIAL_ID_PATTERN`：credential ID 只能由 base64url 字元組成 | 讓 ID 無法被解讀成路徑 |
| `2192982` | `authenticator/storage.py:167–183`（關鍵在第 181 行） | `_credential_file()` 先檢查 ID 的字元，不合法就當作找不到，並補齊註解 | 防止 `../` 這類 ID 讓路徑跳出憑證資料夾 |
| `2192982` | `authenticator/storage.py:115–139`（關鍵在第 137 行） | `load()` 讀出後比對檔案內記錄的 ID 是否完全相同，並補齊註解 | Windows 的檔名比對不分大小寫，不能讓檔案系統決定是不是同一張憑證 |
| `2192982` | `authenticator/tests/test_authenticator.py:228–279` | T7（第 228 行）、T8（第 248 行）、T9（第 262 行） | 驗證追加工作 1 |
| `e35c60a` | `authenticator/bridge.py:7–8`、`176–200` | 新增 `_origin_from_url()`：從網址取出「協定://網域[:埠]」 | 依呼叫者的真實網址算出 origin |
| `e35c60a` | `authenticator/bridge.py:257–303` | `_handle_make()`、`_handle_get()` 改用 `source["frame"].url`，不再讀 `payload["origin"]`，並補齊整個函式的註解 | 符合 WebAuthn §5.8.1：origin 由瀏覽器填入，網頁無法指定 |
| `e35c60a` | `authenticator/tests/test_bridge.py:1–97`（新增） | T10（第 72 行）、T11（第 86 行），註冊、登入兩個入口各測一次 | 驗證追加工作 2 |
| `de413e0` | `authenticator/bridge.py:176–200`、`authenticator/storage.py:115–139`、`167–183`、`authenticator/tests/test_bridge.py`、`authenticator/tests/test_authenticator.py:228–245` | 依第 2 次獨立審查更正與補齊註解（只改註解與 docstring，拿掉 docstring 後的語法樹不變） | 修正寫錯的理由，讓註解符合守則 |
| `c1bd1f0` | `codex/PROTOCOL-GUIDE.html` 第 3、10、11 章 | 說明 bridge 取得 origin 的方式；更新測試數；名詞表新增 binding、frame | 導覽跟上程式的變動；新術語進名詞表 |
| `e19f74a` | `codex/worklog/day-01.md` | 開工段落新增「追加工作 2」（T12、T13 與對齊紀錄）；完工段落記錄第 2 次審查 | 在寫測試之前留下核准紀錄 |
| `3486103` | `authenticator/tests/test_storage.py:40–119` | `_settings()`（第 40 行）、T12（第 60 行，3 種寫法）、T13（第 88 行） | 讓字元檢查與 ID 比對都有測試保護，Linux 的 CI 也偵測得到 |
| `2ba3d1f` | `authenticator/bridge.py:128–169` | 注入腳本不再在 payload 放用不到的 origin，並補齊 `wrapNavigator()` 的註解 | 避免讀者誤以為 origin 來自頁面；行為不變 |
| 完工紀錄 | `codex/REPORTS.md:401–402` | Decision Log 第 54–55 號 | 記錄兩個安全修正 |
| 完工紀錄 | `codex/FN-DSA-PLAN.md` | 日期順延 2 天、勾選 Day 1（含追加的安全修正）、每日流程與分支規則改為指向 `CLAUDE.md` | 讓計畫和實際進度一致 |
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
| T7 | 紅燈（Windows）：`DID NOT RAISE CredentialStoreError`（只差大小寫的 ID 開到憑證 A 的檔案，選中了 A） | 綠燈 |
| T8 | 紅燈（Windows）：`DID NOT RAISE CredentialStoreError`（`../credentials/<A 的 ID>` 解析到憑證 A 的檔案） | 綠燈 |
| T9 | 紅燈（Windows）：`CredentialStoreError: Credential creation excluded by RP`（誤判為重複註冊） | 綠燈 |
| T10 | 紅燈：註冊、登入兩個入口都把頁面自稱的 `http://localhost:3000` 交給 authenticator | 綠燈 |
| T11 | 紅燈：兩個入口交給 authenticator 的 origin 都是 `None` | 綠燈 |
| T12 | 綠燈（實作已在 `2192982`；有效性由破壞檢查證明） | 綠燈 |
| T13 | 綠燈（實作已在 `2192982`；有效性由破壞檢查證明） | 綠燈 |

整體：Python 測試從 14 個增為 32 個，Extension 11 個、Frontend 4 個。
- 從第 2 個 commit 到 `c1bd1f0`，每個 commit 都通過 8 項必跑檢查。
- `e19f74a`、`3486103`、`2ba3d1f` 依使用者決定，commit 前只跑 ruff 與 T12、T13；`2ba3d1f` 只改注入腳本，另外用 `node --check` 確認語法。全套測試由 PR 上的 CI 執行。
- T7–T9 的紅燈只會在 Windows 出現：CI 的 Linux 改用 keyring 儲存，假 keyring 區分大小寫。T13 補上這個缺口。

### 破壞檢查

| 測試 | 怎麼改壞 | 結果 |
|---|---|---|
| T1 | 驗章改回「解析後重新序列化」再算 hash | T1 變紅 |
| T4 | 拿掉 rpId 的檢查 | 只有 T4 變紅 |
| T3 | 恢復「清單裡找不到就改用同網站第一把」 | 只有 T3 變紅 |
| T6 | 拿掉 origin 檢查（`c679adf` 加強斷言後補做） | T6 變紅 |
| T7、T9 | 拿掉 `load()` 裡「ID 完全相同」的比對 | T7、T9 變紅；T8 仍是綠燈（ID 字元檢查擋住了路徑） |
| T8 | 同時拿掉 ID 字元檢查和「ID 完全相同」的比對 | T8 變紅 |
| T10 | 兩個入口改回優先採用 `payload["origin"]` | T10 的兩個入口都變紅；T11 仍是綠燈（它的 payload 沒有 origin） |
| T11 | `_origin_from_url()` 直接回傳完整網址，不去掉路徑與查詢字串 | T10、T11 共 4 個測試全部變紅 |
| T12 | 只拿掉 `_credential_file()` 的字元檢查 | T12 的 3 種寫法全部變紅，錯誤訊息顯示碰到了 `credentials\..\outside.bin` 與資料夾外的 `outside.bin`；T13 仍是綠燈 |
| T13 | 只拿掉 `load()` 的 ID 比對 | T13 變紅（`DID NOT RAISE`）；T12 仍是綠燈 |

每次檢查後都已改回正確的實作；`bridge.py`、`storage.py` 改回後用 SHA-256 比對，和破壞前完全相同。

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

**第 2 次（T7–T11 與 `c679adf`）**：由另一個沒看過實作過程的子代理審查。它用 `git archive` 取出修正前的程式重跑測試，並在記憶體中用 10 種方式改壞實作。

- **結論**：T7–T11 都忠實對應核准的案例，修正前都會失敗，失敗原因和「實作前預期」一致。`c679adf` 的加強正確。沒有發現安全漏洞。
- **逐 commit 驗證**：每個 commit 單獨取出來跑都通過，`c679adf` 21 個、`2192982` 24 個、`e35c60a` 28 個。
- **測試案例沒有被改弱**：T1–T6 的核准列和 `3ba07d6` 的版本逐字相同。

| 審查意見 | 分類 | 處理 |
|---|---|---|
| `_origin_from_url()` 的 docstring 理由寫錯。about:blank、about:srcdoc、blob: 頁面在瀏覽器中有 origin（沿用建立者或內層網址的），真正的理由是只看 frame.url 無法得知。「和瀏覽器算出的 origin 相同」也只對一般 http(s) 頁面成立，sandbox iframe 例外 | 必須修正 | 已更正。commit `de413e0` |
| commit 版本的工作紀錄還沒有 T7–T11 的紅燈與破壞檢查結果 | 必須修正 | 已補在本段的「測試結果」「破壞檢查」 |
| 字元檢查沒有測試保護：只拿掉它時 28 個測試全綠。T8 會被讀出後的比對擋下，但那時已經讀過資料夾外的檔案 | 建議（優先） | 使用者核准 T12，已新增並做破壞檢查。commit `3486103` |
| CI 用 keyring 後端，假 keyring 區分大小寫，T7、T9 在 CI 上抓不到「ID 比對被拿掉」 | 建議 | 使用者核准 T13，已新增並做破壞檢查（`3486103`）；T7 的 docstring 已寫明這點（`de413e0`） |
| 註解不完整：假 authenticator 與 `_call_handler()` 缺說明、T11 沒寫依據、storage 把 ID 的來源說成只有 RP | 建議 | 已補齊。commit `de413e0` |
| 開工段落「T7–T9 的問題來自 Windows 檔案系統不分大小寫」對 T8 不正確 | 建議 | 開工段落已加註更正 |
| 注入腳本仍在 payload 放 origin，但 bridge 已經不用 | 建議（可選） | 使用者選擇刪除。commit `2ba3d1f` |
| `__pqListCredentials` 沒有 origin 檢查；`delete()` 沒有確認 ID 完全相同；Extension 採用頁面傳來的 origin；crossOrigin 固定為 false | 建議（既有問題） | 記入待辦清單 |
| 名詞表沒有 frame、binding | 建議 | 已新增。commit `c1bd1f0` |
| `c0e3000` 的訊息只寫「T7–T11 與對齊紀錄」，實際上也加了第 1 次審查的完工段落與「更正」註記 | 輕微 | 在此說明，不改寫已 commit 的歷史 |

審查者另外查過、確認不是問題的項目：
- 正規表示式只接受 ASCII，也不接受結尾換行。
- 這台 Windows 11 上，`NUL.bin` 這類保留裝置名加上副檔名，只是一般路徑。
- 超長 ID 只會被當作找不到。
- 既有憑證的 ID 都是 `secrets.token_bytes(32)` 產生的 43 字元 base64url，不會讀不到。
- `http://localhost:3000@evil.example/` 會正確得到 evil.example。
- 讀取 frame.url 時的時間差無法被利用。

### 待辦清單（中途發現、今天不處理）

- RP 尚未檢查 signCount 是否遞增（WebAuthn §7.2），也沒有檢查 authenticatorData 的 UP／UV flags。
- Python authenticator 在挑選憑證之前就先要求使用者驗證：找不到憑證時，使用者會先看到 Windows Hello 視窗才收到錯誤。Extension 是先挑憑證再驗證，之後可以考慮讓兩邊一致。
- 新增 `tests/` 資料夾時，要同步加進 `pyproject.toml` 的 `testpaths`、`CLAUDE.md` 與 CI 的 ruff 路徑。
- 前端 eslint 提示 baseline-browser-mapping 的資料過舊；升級依賴要先徵得使用者同意。
- RP 的 CORS 設定允許任何網站呼叫 API（`rp_server/app.py` 的 `CORS(app)` 預設允許所有來源），惡意網站可以替任何帳號索取登入題目。
- Python bridge 的 `__pqListCredentials` 沒有任何 origin 檢查。在 bridge 開的 Chromium 裡，任何網站都能呼叫 `window.__pqListCredentials()`，取得所有憑證的 ID、rpId 與使用者名稱。這是修正前就存在的問題，威脅模型和今天修的 origin 問題相同。
- `CredentialStore.delete()` 沒有確認 ID 完全相同。在 Windows 上，大小寫不同的 ID 會刪掉另一張憑證的加密檔，index 卻還留著它，之後讀取這張憑證都會失敗。目前只有測試會呼叫 `delete()`。
- Extension 的 background 採用頁面傳來的 `payload.origin`（`extension/src/background/authenticator.ts:229`、`:313`）。目前 `isTrustedSender()` 只接受 demo.yubico.com 的頁面，所以風險低。D5 開放 `http://localhost:3000` 時，建議改用 Chrome 提供的 `sender.url` 推出 origin，做法同 Python bridge。
- clientDataJSON 的 `crossOrigin` 固定為 false，bridge 也沒有檢查跨網域 iframe 的 Permissions Policy。sandbox iframe 在瀏覽器中的 origin 是 "null"，bridge 仍會回傳網址的 origin。
