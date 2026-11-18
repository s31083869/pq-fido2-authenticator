# Day 3：F03 + F04 RP Server 宣告與接受 FN-DSA

| 項目 | 內容 |
|---|---|
| 日期 | 2026-11-18 |
| 分支 | `day-03`（從 `origin/main` 39d61e4 開出） |
| 狀態 | 完工：T1–T5 與依獨立審查的兩項輕微修正都已完成；PR #5 的 CI 全部通過，已於 11/18 合併 |

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

- `hosted_algorithms` 沒有檢查每個編號都在共用表裡。若有人在設定裡放 -7，RP 會對外宣告 -7。開工時的行為是「接受 -7 的註冊，但登入時 `_cose_to_oqs()` 一律回 400」。Day 3 加了長度檢查後，-7 在共用表查不到長度，註冊一律回 400 `Invalid public key`。這個分支是安全的（一律拒絕），但核准的測試沒有涵蓋它，錯誤訊息也不夠精確。建議讓 `RPSettings` 在啟動時就拒絕共用表以外的編號，這個分支就不會再走到。
- 登入驗章時，liboqs-python 遇到太長的公鑰會丟出 `ValueError`（對齊時實測），`services.py` 的驗章區塊沒有接住，回應會是 500。Day 3 之後新註冊的憑證都已檢查過長度；Day 3 之前就存在 DB 的資料仍可能觸發。
- （獨立審查，既有問題）`verify_registration_payload()` 有幾種格式錯誤會變成 500，不是 400：
  - COSE_Key 不是 map 時，`credential_public_key.get` 會丟 `AttributeError`。
  - clientDataJSON 或 CBOR 格式錯誤。
  - alg 用浮點數 `-49.0` 時，仍會通過 `hosted_algorithms` 和長度表的檢查。
  函式說明寫「任何一項不符都以 400 中止」，容易讓人以為已經涵蓋這些情況。
- （獨立審查，既有問題）註冊時沒有檢查 flags 的 UP 位元（WebAuthn §7.1 要求 UP 為 1），也沒有比對 payload 的 `rawId` 和 authData 裡的 credentialId 是否相同。
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
- 獨立審查後，使用者同意一併處理兩項輕微意見（11/18）：T2 加上「DB 剛好一筆」的計數斷言（加強，不是改弱），以及更正 `verify_registration_payload()` 說明的依據。

---

## 完工

### 實際修改

行號以 Day 3 最後一個 commit 的版本為準。

| commit | 檔案:行號 | 改了什麼 | 目的 |
|---|---|---|---|
| `2d7aae3` | `codex/worklog/day-03.md`、`codex/worklog/day-02.md:7` | 新增本文件的開工段落；day-02 狀態補記 PR #4 的 CI 已通過 | 在實作前留下測試案例與對齊紀錄 |
| `9cb674b` | `rp_server/config.py:15–24` | 補上 `RPSettings` 的類別說明，逐一說明各欄位 | 依守則補齊修改到的類別的註解 |
| `9cb674b` | `rp_server/config.py:36–45` | `hosted_algorithms` 預設值改為 `[-49, -48, -50, -54, -55]`，註解說明它同時決定宣告與接受、順序依 D6 | F03：RP 宣告並接受 FN-DSA |
| `9cb674b` | `rp_server/tests/test_app.py:39–66` | T1 | 驗證 `/register/options` 的五個演算法與順序 |
| `9cb674b` | `rp_server/tests/test_authentication_verify.py:164–165` | T7 的說明改為現況，指向 T2 | 拿掉「Day 3 才開放 FN-DSA」這句過時的說明 |
| `dac1c32` | `rp_server/tests/test_registration_verify.py:1–209`（新增，`3cbd66c`、`afb5b9d` 擴充到 275 行） | 組 attestationObject 的輔助函式（`_cose_key` 第 54 行、`_attestation_object` 第 66 行、`_register` 第 89 行、`_credential_count` 第 122 行）、T2（第 129 行）、T3（第 193 行） | F04：FN-DSA 憑證經過 RP 真正的註冊檢查存進 DB，並能登入驗章 |
| `3cbd66c` | `rp_server/services.py:19`、`26–33` | 匯入 `ALGORITHMS`；新增 `COSE_KTY_AKP` 與從共用表產生的 `COSE_TO_PUBLIC_KEY_BYTES` | 長度的唯一來源是共用表（D3） |
| `3cbd66c` | `rp_server/services.py:97–171` | `verify_registration_payload()` 新增 kty 檢查（第 154–157 行）與公鑰長度檢查（第 159–166 行），並補齊整個函式的註解 | 格式錯誤的公鑰在註冊時就被擋下 |
| `3cbd66c` | `rp_server/tests/test_registration_verify.py:1–10`、`215–275` | 模組說明補上 T4、T5；T4（第 225 行）、T5（第 253 行） | 驗證兩項新檢查 |
| `4219bb9` | `codex/PROTOCOL-GUIDE.html:760`、`766`、`781`、`793`、`805`、`810`、`1377` | 預設宣告順序改為五個演算法；第 8 步加上 kty 與長度檢查；註冊案例的參數；Python 測試數改為 80；補上 Day 3 進度 | 導覽跟上程式 |
| `afb5b9d` | `rp_server/tests/test_registration_verify.py:150–151` | T2 加上 `_credential_count(settings) == 1` | 依獨立審查，讓斷言貼近核准的「DB 新增一筆憑證」 |
| `bf98f18` | `rp_server/services.py:104–108` | 函式說明更正依據：kty 與長度依 RFC 9964、RFC 9052 與共用表；註明無法解析的輸入目前會是 500 | 依獨立審查，只改註解 |
| 完工紀錄 | `codex/REPORTS.md` | Decision Log 第 60 號 | 記錄今天的決定 |
| 完工紀錄 | `codex/FN-DSA-PLAN.md:96–98` | 勾選 Day 3，註明驗章的部分在 Day 2 已完成 | 讓計畫和實際進度一致 |
| 完工紀錄 | `codex/worklog/day-03.md` | 完工段落；開工段落的待辦清單更新 | 本段 |

協議導覽沒有新增名詞：今天用到的 AKP、kty、COSE_Key 都已在第 11 章。

### 測試結果（實作前 → 實作後）

| 測試 | 實作前 | 實作後 |
|---|---|---|
| T1 | 紅燈：`AssertionError`，`pubKeyCredParams` 只有三筆 | 綠燈 |
| T2 | ML-DSA 三個綠燈；FN-DSA-512、FN-DSA-1024 紅燈：註冊回 400 `{'message': 'Unsupported algorithm'}` | 綠燈（5 個） |
| T3 | 綠燈（回歸保護；有效性由破壞檢查證明） | 綠燈 |
| T4 (a)–(d) | 紅燈：4 個都是 `assert 200 == 400` | 綠燈 |
| T5 (a)(b) | 紅燈：2 個都是 `assert 200 == 400` | 綠燈 |

**T2 的紅燈是事後重現的。** 實作順序是先完成第一項（`9cb674b` 改 config，同時寫 T1），才寫 T2。T2 寫好時 config 已經包含 -54/-55，所以一寫好就是綠燈。為了確認「實作前預期」，把 `rp_server/config.py` 暫時換成開工 commit `2d7aae3` 的版本重跑：結果是 2 失敗、4 通過，失敗的正是 FN-DSA-512、FN-DSA-1024，錯誤訊息是 `Unsupported algorithm`，和開工段落的預期完全一致。跑完已換回，並用 SHA-256 確認相同。T1、T4、T5 都是先寫測試、確認紅燈後才實作。

整體：Python 測試從 67 個增為 80 個，Extension 11 個、Frontend 4 個。7 個 commit（含依審查追加的 `afb5b9d`、`bf98f18`）前都跑過 8 項必跑檢查並全部通過。

### 破壞檢查

| 測試 | 怎麼改壞 | 結果 |
|---|---|---|
| T1 | `hosted_algorithms` 改回 `[-49, -48, -50]` | `test_app.py` 只有 T1 變紅（當時 T2 尚未寫；T2 的 FN-DSA 會跟著變紅，已在上面的紅燈重現中確認） |
| T3 | 拿掉 `verify_registration_payload()` 中「alg 必須在 `hosted_algorithms`」的檢查 | `test_registration_verify.py` 只有 T3 變紅 |
| T4 | 拿掉公鑰長度檢查 | `rp_server/tests` 只有 T4 (a)–(d) 變紅，共 4 個 |
| T5 | 拿掉 kty 檢查 | `rp_server/tests` 只有 T5 (a)(b) 變紅，共 2 個 |

每次檢查後都已改回正確的實作，並用 SHA-256 確認和破壞前完全相同。

### 獨立審查

由沒看過實作過程的子代理審查 `origin/main..4219bb9`，以開工段落核准的測試案例表為標準。

**結論**：沒有必須修正的項目。T1–T5（含 T4 (d)）都忠實對應核准的案例，預期值都來自外部依據。

- **紅燈重現**：
  - 在 `2d7aae3` 放進 T1、T2、T3：3 失敗、8 通過。失敗的是 T1 與 T2 的兩個 FN-DSA，錯誤訊息是 `Unsupported algorithm`。
  - 在 `dac1c32` 放進 T4、T5：6 失敗、6 通過，6 個都是 `assert 200 == 400`。
  - 兩者都和開工段落的「實作前預期」一致。
- **預期值查證**：審查者用規格的編碼公式獨立算出公鑰長度。
  - Falcon：1 + 14n/8，n = 512 得 897，n = 1024 得 1793。
  - ML-DSA：32 + 320k，k = 4、6、8 依序得 1312、1952、2592。
  - 結果都和測試裡寫死的數值、共用表相同。
- **liboqs 行為**：獨立重現了對齊紀錄問題 2 的說法：公鑰太長時丟出 `ValueError`，太短時 `verify()` 回 False。
- **破壞檢查**：用 18 種方式改壞實作，15 種被抓到。沒抓到的 3 種：
  - M11：長度表查不到時改成放行。預設設定走不到這個分支，已記入待辦清單。
  - M12：把 alg 檢查移到 kty 和長度檢查之後。每個測試都只有一項錯誤，順序不影響結果，不算缺陷。
  - M13：拿掉公鑰的 bytes 型別檢查。這是既有檢查，不在核准範圍。
- **逐 commit 驗證**：5 個 commit 單獨取出，pytest（67 → 68 → 74 → 80 → 80）、ruff check、ruff format 都通過。
  - 這個範圍沒有改到 `extension/`、`frontend/`，所以這兩個只在 HEAD 跑一次，也都通過。

| 審查意見 | 分類 | 處理 |
|---|---|---|
| T2 沒有直接斷言「DB 新增一筆」，只用 `session.get` 查得到。DB 是全新的，查得到就表示有一筆，加上計數會更貼近核准的文字 | 輕微 | 使用者同意加強（不是改弱）。加上 `_credential_count(settings) == 1`，並做破壞檢查：讓 `store_credential()` 多存一筆，加強後的 T2 五個都變紅，加強前的 T2 仍然全綠。commit `afb5b9d` |
| `verify_registration_payload()` 的說明寫「依 WebAuthn §7.1 依序檢查……kty 必須是 AKP、公鑰長度必須符合」，但 kty 與長度的依據是 RFC 9964、RFC 9052 與共用表，不是 §7.1（`services.py:104–106`） | 輕微 | 使用者同意，已更正（只改註解）。commit `bf98f18` |
| 既有問題：COSE_Key 不是 map、clientDataJSON 或 CBOR 格式錯誤時回 500；alg 為浮點數 `-49.0` 時會通過檢查 | 建議 | 記入待辦清單 |
| 既有問題：註冊時沒有檢查 UP 位元，也沒有比對 `rawId` 與 authData 的 credentialId | 建議 | 記入待辦清單 |
| 完工段落把 T2 標在第 128 行（parametrize 裝飾器），其他測試標的都是 `def` 那一行 | 輕微 | 已更正為第 129 行 |

審查者另外確認沒有問題的項目：
- 核准的測試沒有被改弱：`dac1c32` 到 `3cbd66c` 之間，T2、T3 沒有被改動。
- 長度表查不到時一律拒絕，這是安全的做法。
- 修改到的函式與類別，註解都已補齊。
- 開工段落與完工段落引用的行號都正確。
- 協議導覽和程式一致。
- 只改了「預計修改」列出的檔案，沒有動到使用者資料檔與第三方資料夾。
