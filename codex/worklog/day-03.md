# Day 3：F03 + F04 RP Server 宣告與接受 FN-DSA

| 項目 | 內容 |
|---|---|
| 日期 | 2026-11-18 |
| 分支 | `day-03`（從 `origin/main` 39d61e4 開出） |
| 狀態 | 開工：測試案例已核准，實作中 |

---

## 開工

### 開工前補記

- Day 2 的 PR #4 三項 CI（Python、Extension、Frontend）都已通過，已於 11/17 合併。`day-02.md` 的狀態欄原本寫「待 PR 的 CI 結果」，今天一併改為已通過。

### 今日目標

依序完成，每一項各自一個 commit（訊息格式 `Day 3: …`）：

1. RP 的 `hosted_algorithms` 預設值從 `[-49, -48, -50]` 改為 `[-49, -48, -50, -54, -55]`（F03；順序依 D6，Decision Log 第 47 號）
2. 為 RP 的註冊驗證（`/register/verify`）補上測試：目前**完全沒有**任何測試走過這條路。用真的 liboqs 金鑰組出 attestationObject，確認五個演算法都能註冊、存進 DB，再用同一把金鑰登入驗章成功（F04）
3. 註冊時檢查 COSE_Key 的 `kty` 是否為 7（AKP），以及公鑰長度是否等於共用表的 `publicKeyBytes`

**完成標準**（`FN-DSA-PLAN.md` Day 3）：RP 能宣告、接受並驗證 FN-DSA。

### 架構背景

#### 1. RP 在註冊和登入中各管哪一段

| 階段 | RP 做什麼 | 程式 | 和演算法有關的部分 |
|---|---|---|---|
| 註冊第 2 步 | 回傳註冊參數 | `rp_server/app.py:141–143` | `pubKeyCredParams` 由 `hosted_algorithms` 逐一產生，順序就是 RP 的偏好 |
| 註冊第 8 步 | 檢查並存下憑證 | `rp_server/services.py:89–129` 的 `verify_registration_payload()` | 取出 `credentialPublicKey[3]`（alg），**必須在 `hosted_algorithms` 裡**（`:119–121`），否則 400 `Unsupported algorithm` |
| 登入第 8 步 | 驗章 | `rp_server/services.py:132–194` | 用 DB 存的 alg 查共用表得到 liboqs 名稱（`_cose_to_oqs()`，Day 2 已改好） |

所以 RP 這邊**只有一個開關**：`hosted_algorithms`。它同時決定「對外宣告哪些演算法」和「註冊時接受哪些演算法」。登入驗章那一段在 Day 2 就已經認得 -54/-55 了（T7 已用真的 Falcon 簽章測過），只是 DB 裡一直不可能出現 FN-DSA 憑證，因為註冊這一關擋著。

`FN-DSA-PLAN.md` Day 3 的第二項「驗章時從共用表取得 liboqs 名稱」在 Day 2 已經完成，今天不用再改。

#### 2. 改完之後，各個 authenticator 的行為

RP 宣告的順序是 `[-49, -48, -50, -54, -55]`。WebAuthn 規定 `pubKeyCredParams` 依 RP 偏好由高到低排列，authenticator 選「第一個自己支援的」。

| 誰 | 支援哪些 | 預設會選 | 會不會壞 |
|---|---|---|---|
| Python authenticator | 五個（Day 2 起） | -49 | 不會，行為不變 |
| Chrome Extension | 只有 ML-DSA（Day 6 才加） | -49 | 不會：`selectAlgorithm()`（`extension/src/background/authenticator.ts:41–56`）跳過不認得的 -54/-55 |
| 前端網頁 | 選單只有 ML-DSA（Day 5 才加） | 把使用者選的 ML-DSA 排到最前面 | 不會 |

也就是說，今天之後**預設的註冊結果完全不變**，FN-DSA 只有在「有人把 -54/-55 排到前面」時才會被選到。Day 5 前端選單加入 FN-DSA 後，使用者才能從網頁上選它。

#### 3. 為什麼要自己組 attestationObject

`/register/verify` 收到的是 authenticator 產生的 attestationObject。測試不想依賴 authenticator 的程式（RP 和 authenticator 是不同角色，D3 / Decision Log 第 57 號的同一個理由），所以在 RP 的測試裡依 WebAuthn 規格自己組：

```
attestationObject = CBOR { "fmt": "none", "attStmt": {}, "authData": authData }

authData（WebAuthn §6.1）
  0–31   rpIdHash      = SHA-256("localhost")
  32     flags         = 0x45（UP 0x01 | UV 0x04 | AT 0x40）
  33–36  signCount     = 0，大端序
  37–52  AAGUID        = 16 個 0
  53–54  credIdLength  = 32，大端序
  55–86  credentialId  = 32 bytes 隨機值
  87–    credentialPublicKey = CBOR { 1: 7, 3: alg, -1: 公鑰 }（RFC 9964 AKP）
```

公鑰是用 liboqs 真的產生的，之後再用對應的私鑰簽一次登入，所以這條測試同時滿足 `CLAUDE.md`「真實密碼學」的「產生金鑰 → 簽章 → RP 驗章」，而且這次憑證是**經過 RP 的註冊檢查**存進 DB 的，不是像 Day 2 的 T7 那樣直接寫進 DB。

### 預計修改

| 檔案 | 預計修改 | 對應項目 |
|---|---|---|
| `rp_server/config.py:26–29` | `hosted_algorithms` 預設值加入 -54、-55，補齊 `RPSettings` 的註解 | 1 |
| `rp_server/tests/test_app.py` | T1 | 1 |
| `rp_server/tests/test_registration_verify.py`（新增） | T2–T5；含組 attestationObject 的輔助函式 | 2、3 |
| `rp_server/services.py:89–129` | `verify_registration_payload()` 加入 kty 與公鑰長度檢查，並補齊整個函式的註解 | 3 |
| `rp_server/tests/test_authentication_verify.py:164` | T7 的說明「Day 3 才開放 FN-DSA」改成現況 | 文件 |
| `codex/PROTOCOL-GUIDE.html` 第 4 章第 2、8 步、第 781 行附近 | 預設宣告順序改為 -49、-48、-50、-54、-55；第 8 步加上 kty 與長度檢查 | 文件 |
| `codex/worklog/day-02.md` | 狀態改為 CI 已通過 | 文件 |
| `codex/FN-DSA-PLAN.md` | 勾選 Day 3 | 文件 |

### 測試案例（待你核准）

| 編號 | 情境 | 預期結果 | 依據 | 實作前預期 |
|---|---|---|---|---|
| T1 | 用預設設定呼叫 `/register/options` | `pubKeyCredParams` 剛好是 `[-49, -48, -50, -54, -55]` 五筆，順序相同，每筆的 `type` 都是 `"public-key"` | workflow.md F03 驗收標準「`pubKeyCredParams` 包含 -54/-55」；D6（Decision Log 第 47 號）規定的順序；WebAuthn §5.4 `pubKeyCredParams` 依偏好排序 | 紅燈（目前只有三筆） |
| T2 | 對共用表的每個演算法（預設設定）：用 liboqs 產生金鑰，組出 attestationObject 送 `/register/verify`；接著 `/authenticate/options` 取得 challenge，用私鑰對 `authenticatorData ‖ SHA-256(clientDataJSON)` 簽章，送 `/authenticate/verify` | 註冊回 200；DB 新增一筆憑證，`algorithm` 等於該演算法的 `coseAlg`、`public_key` 等於公鑰的 base64url；登入回 200 | workflow.md F04 驗收標準「FN-DSA credential 可被存入 DB，assertion 可驗章成功」；F14「註冊後保存 algorithm=-54/-55」；WebAuthn §7.1、§7.2；`CLAUDE.md`「真實密碼學」 | ML-DSA 三個綠燈；FN-DSA-512、FN-DSA-1024 紅燈（註冊回 400 `Unsupported algorithm`） |
| T3 | RP 設定為 `hosted_algorithms=[-49, -48, -50]`（不含 FN-DSA），送出 alg 為 -54 的註冊 | 回 400 `Unsupported algorithm`，DB 沒有新增憑證 | WebAuthn §7.1：RP 必須確認憑證公鑰的 alg 是它在 `pubKeyCredParams` 中提供的其中一個；F16「RP 未宣告就不可接受」的 RP 端 | 綠燈（回歸保護；有效性由破壞檢查證明） |
| T4 | 預設設定下，公鑰長度不符：(a) alg -54、公鑰 896 bytes；(b) alg -55、公鑰 897 bytes（FN-DSA-512 的長度）；(c) alg -49、公鑰 1312 bytes（ML-DSA-44 的長度）；(d) alg -54、公鑰 1793 bytes（太長，FN-DSA-1024 的長度） | 都回 400 `Invalid public key`，DB 沒有新增憑證 | 共用表的 `publicKeyBytes`，來源為 Falcon v1.2 第 3.11 節（897／1793）與 FIPS 204 Table 2（1952）；這三個演算法的公鑰長度都是固定的。(d) 是對齊時追加的：公鑰太長時 liboqs-python 驗章會丟 `ValueError`，登入變成 500（見對齊紀錄問題 2） | 紅燈（目前不檢查長度，回 200） |
| T5 | 預設設定下，COSE_Key 的 kty 不對：(a) kty 為 2（EC2）；(b) 沒有 kty 欄位；其餘欄位都正確（alg -54、897 bytes 公鑰） | 都回 400 `Invalid public key`，DB 沒有新增憑證 | RFC 9964：ML-DSA 的 COSE_Key 使用 AKP（kty = 7），draft-ietf-cose-falcon-04 的 FN-DSA 沿用 AKP；RFC 9052 §7：kty 是 COSE_Key 必填的欄位 | 紅燈（目前不檢查 kty，回 200） |

**破壞檢查**：
- T1：`hosted_algorithms` 改回三筆，T1 變紅，T2 的 FN-DSA 兩個也變紅。
- T3：拿掉 `verify_registration_payload()` 裡「alg 必須在 `hosted_algorithms`」的檢查，T3 必須變紅。
- T4、T5：分別拿掉長度檢查、kty 檢查，對應的案例必須變紅。

### 待你決定（已決定，見對齊紀錄）

1. **註冊時是否檢查 kty 與公鑰長度**（Day 2 待辦清單第 1 項）：建議「是」，加入 T4、T5。使用者採用。
   - 理由：今天本來就要讓 RP 開始接受 FN-DSA 註冊，這個函式正好是今天的修改範圍。目前公鑰只檢查「是 bytes」，長度錯的公鑰也會存進 DB，要等到登入時才以 `Invalid signature` 失敗，和 Day 2 確認問題 2 是同一類「註冊時看不出來、登入才爆」的錯誤。
   - 不做的話：今天只做 T1–T3，這一項留在待辦清單，之後另外排。
   - 注意：這個檢查擋的是「格式錯的公鑰」。attestation 為 none，RP 仍然無法確認 authenticator 真的持有對應的私鑰；這是 PoC 的既有設計，不在今天處理。

### 待辦清單（中途發現、今天不處理）

- `hosted_algorithms` 沒有檢查每個編號都在共用表裡。若有人在設定裡放 -7，RP 會宣告並接受 -7 的註冊，但登入時 `_cose_to_oqs()` 一律回 400，這個帳號永遠無法登入。可以讓 `RPSettings` 在啟動時就拒絕共用表以外的編號。
- 沿用 Day 1、Day 2 的待辦清單。

### 對齊紀錄

- 決定：註冊時檢查 kty 與公鑰長度，加入 T4、T5（「待你決定」第 1 點採建議做法，11/18）。
- 理解確認（使用者回答三題）：
  - 「RP 改 `hosted_algorithms`，同時決定宣告和接受哪些演算法」：已對上。
  - 「預設註冊結果不變，因為只改註冊檢查、沒改註冊內容」：有落差。Claude 補充：註冊參數其實有變，`pubKeyCredParams` 從三筆變五筆。結果不變的真正原因是**順序**：-54/-55 排在 ML-DSA 後面，authenticator 挑「第一個自己支援的」，Python authenticator 挑到 -49；Extension 不認得 -54/-55，直接跳過；前端又把使用者選的 ML-DSA 排到最前面。
  - 「T7 把憑證直接寫進 DB，沒有經過註冊檢查」：已對上。Claude 補充：T2 從註冊參數一路走到登入驗章，FN-DSA 憑證第一次經過 RP 真正的註冊檢查進入 DB。
- 使用者表示之前一直以為「使用者選哪個就用哪個」，請 Claude 詳細說明演算法是怎麼挑的。Claude 說明：
  - 演算法經過三方：RP 提供清單（`app.py:141–143`），前端只能調整順序（`frontend/src/pages/index.tsx:194–197`），由 authenticator 做最後決定。
  - authenticator 照順序挑第一個自己支援的（Python `authenticator/service.py:323–327`、Extension `authenticator.ts:41–56`），依據是 WebAuthn §6.3.2 authenticatorMakeCredential。
  - 「選哪個就用哪個」只是表面現象：前端把使用者選的排到第一個，而 authenticator 剛好支援它。
  - 以 Day 5 之後、Day 6 之前的情況舉反例：使用者選 -54，Extension 不認得，會選到 -49。
  - 前端在 RP 沒有提供某個演算法時也會把它塞進清單，可能被 RP 以 `Unsupported algorithm` 拒絕。這是 Day 5 要修的問題。
- 使用者請 Claude 詳細說明例子 4（RP 沒提供 -54，前端卻把它塞進清單）。Claude 逐步說明：
  - 走到失敗前，已經發生的事：使用者已經過 Windows Hello，authenticator 已產生 Falcon-512 金鑰，並把私鑰存進自己的儲存區（`authenticator/service.py:153–164`）。
  - RP 在 `services.py:119–121` 擋下，回 400。authenticator 留下一張 RP 不知道的孤兒憑證；WebAuthn 本來就允許這種情況，不算 bug。
  - 前端和 RP server 都屬於 RP 這一方，這是兩者對外的說法不一致。
  - RP server 不能相信前端送來的任何東西（JS 可以被改，請求也可以自己組），所以 T3 要確保 server 這一關擋得住。
  - 目前的前端選單只有 ML-DSA，都在 `hosted_algorithms` 裡，所以這個問題現在不會發生；Day 5 選單加入 FN-DSA 後才可能發生。
- 確認問題：
  - 問題 1（`hosted_algorithms` 改成 `[-54, -49, -48, -50]`，前端不重排，各會選哪個）：使用者回答「-54、-49，因為 Extension 是在 Yubico 上 demo，他們還不支援 FN-DSA」。答案對，理由有落差。Claude 補充：
    - demo.yubico.com 是 Extension 目前唯一攔截的**網站**（RP），不是 authenticator。
    - Extension 選 -49，是因為它**自己**只支援 ML-DSA（`authenticator.ts:19` 的 `SUPPORTED_ALGORITHMS`），WASM 裡也還沒有 Falcon（Day 7）。這和面對哪個網站無關。
    - 另外，Extension 目前只攔截 demo.yubico.com，要到 Day 8（D5）才開放 localhost，所以現在其實還碰不到我們的 RP。
  - 問題 2（alg 寫 -55、公鑰卻是 897 bytes，沒有長度檢查時會怎樣）：使用者回答「註冊會成功，登入時無法正確驗證」。已對上。Claude 補充：
    - 實際用 liboqs 0.14.0 試過：用 Falcon-1024 驗章器搭配 897 bytes 的公鑰，`verify()` 回傳 False，RP 回 400 `Invalid signature`。
    - 反過來，公鑰**太長**時（-54 配 1793 bytes），liboqs-python 直接丟出 `ValueError: byte string too long`。`services.py:185–188` 沒有接住這個例外，登入會變成 500 錯誤。
    - 在註冊時擋下比較好：錯誤在源頭就被發現，訊息清楚，DB 裡也不會留下一張永遠無法登入的憑證。
  - 問題 3（T3 為什麼一開始就是綠燈，怎麼證明有用）：使用者描述了「拿掉限制前後各跑一次、觀察差別」。方向對，Claude 補充：
    - 綠燈的原因：`services.py:119–121` 的檢查早就存在，T3 測的是既有行為（回歸保護），不是新功能。
    - 證明有用的方法是破壞檢查：暫時把**實作**裡的這個檢查拿掉，T3 必須變紅；之後改回原樣，並用 SHA-256 確認和破壞前相同。
    - 改壞的是實作，不是測試的設定。紅燈證明 T3 真的依賴這個檢查，不是不管怎樣都會過。
- 測試案例 T1–T5：使用者已於 11/18 核准，並同意在 T4 追加 (d)「公鑰太長」。

---

## 完工

（待完成後填寫）
