# Day 2：F01 + F02 共用演算法表

| 項目 | 內容 |
|---|---|
| 日期 | 2026-11-17 |
| 分支 | `day-02`（從 `origin/main` 7020c73 開出） |
| 狀態 | 開工：對齊完成，測試案例已核准，實作中 |

---

## 開工

### 今日目標

依序完成，每一項各自一個 commit（訊息格式 `Day 2: …`）：

1. 建立共用演算法表 `shared/pq-algorithms.json`：五個演算法（ML-DSA-44/65/87、FN-DSA-512/1024），欄位為 `label`、`coseAlg`、`oqsName`、`publicKeyBytes`、`privateKeyBytes`、`signatureBytes`、`signatureLengthFixed`、`status`（F01、F02）
2. 新增 Python 讀取模組 `shared/pq_algorithms.py`：讀入並檢查這份表，RP 與 authenticator 共用
3. RP（`rp_server/services.py`）與 authenticator（`authenticator/pqcrypto.py`）的 COSE → liboqs 對應改成從共用表產生，不再各自寫死
4. 新增測試資料夾 `shared/tests/`，同步加進 `pyproject.toml` 的 `testpaths`、CI 與 `CLAUDE.md` 的 ruff 路徑

**完成標準**（`FN-DSA-PLAN.md` Day 2）：Python 兩端的 mapping 都改從共用表讀取，既有測試通過。

### 架構背景

#### 1. 為什麼要一份「共用」的表

一個演算法在本專案裡有好幾個名字，各層用的不一樣：

| 誰在用 | 用什麼名字 | 例子 |
|---|---|---|
| WebAuthn 訊息（`pubKeyCredParams`、`credentialPublicKey[3]`、RP 的 DB） | COSE 演算法編號 | `-54` |
| liboqs（真正做數學運算的函式庫） | liboqs 名稱 | `Falcon-512` |
| 給人看的介面、文件 | 標準名稱 | `FN-DSA-512` |

目前「COSE 編號 → liboqs 名稱」這張對照表在 Python 端**寫了兩次**：
- authenticator：`authenticator/pqcrypto.py:14–18` 的 `COSE_ALG_TO_OQS`
- RP：`rp_server/services.py:195–199` 的 `COSE_TO_OQS`

之後 Extension 的 TypeScript（Day 6）和 WASM 的 C bridge（Day 7）還各有一份。只要其中一份漏改，就會出現「RP 宣告了 -54，authenticator 卻不認得」或「兩邊把 -54 對到不同演算法」這種錯誤，而且不一定會有錯誤訊息。D3 決定把它收成**一份** JSON，各層都從這裡讀；以後 FIPS 206 發布要遷移時，也只改這一個地方。

#### 2. 表裡每個欄位的意義與數值來源

| 演算法 | `coseAlg` | `oqsName` | 公鑰 | 私鑰 | 簽章 | 長度固定 | `status` |
|---|---:|---|---:|---:|---:|---|---|
| ML-DSA-44 | -48 | `ML-DSA-44` | 1312 | 2560 | 2420 | 是 | `standard` |
| ML-DSA-65 | -49 | `ML-DSA-65` | 1952 | 4032 | 3309 | 是 | `standard` |
| ML-DSA-87 | -50 | `ML-DSA-87` | 2592 | 4896 | 4627 | 是 | `standard` |
| FN-DSA-512 | -54 | `Falcon-512` | 897 | 1281 | 752（上限） | 否 | `provisional` |
| FN-DSA-1024 | -55 | `Falcon-1024` | 1793 | 2305 | 1462（上限） | 否 | `provisional` |

數值的外部依據：
- **ML-DSA 的 COSE 編號**：RFC 9964（ML-DSA for JOSE and COSE），IANA 已正式分配，所以 `status` 是 `standard`。
- **ML-DSA 的大小**：FIPS 204 Table 2。ML-DSA 的簽章長度是固定的。
- **FN-DSA 的 COSE 編號**：draft-ietf-cose-falcon-04 申請中的編號，IANA 尚未分配（D1），所以 `status` 是 `provisional`（暫定）。
- **FN-DSA 的公鑰、私鑰大小**：Falcon 第三輪規格 v1.2 的金鑰編碼（3.11 節）。
- **FN-DSA 的簽章大小**：我們用的是不補滿的壓縮格式（D2，規格 3.11.6），**每次簽章的長度都不一樣**。752／1462 是 liboqs 為這個格式訂的上限，出自 liboqs 的演算法資料表 `docs/algorithms/sig/falcon.yml`，與 liboqs 0.14.0 標頭檔 `sig_falcon.h` 的 `OQS_SIG_falcon_512_length_signature` 相同。所以 `signatureBytes` 對 FN-DSA 的意思是「最多這麼長」，`signatureLengthFixed` 就是用來標明這一點；Day 6 的 Extension 會依這個欄位決定緩衝區大小。

#### 3. Python 怎麼讀這份表

新增 `shared/pq_algorithms.py`。程式啟動時讀一次 JSON，檢查格式，轉成不可修改的資料物件；任何一筆有問題（缺欄位、型別錯、COSE 編號或 liboqs 名稱重複）就直接丟 `ValueError`，不讓程式帶著錯的表繼續跑。RP 與 authenticator 都 `import` 這個模組，各自原本的對照表改成從它產生。

為什麼放在 `shared/`，而不是放在 authenticator 讓 RP 去 import：RP 和 authenticator 在協議中是**兩個不同的角色**（真實世界裡是不同公司寫的程式），RP 不應該依賴 authenticator 的程式碼。兩者共用的只有「演算法的定義」，所以放在中立的位置。

#### 4. 切換之後，行為會變什麼（需要你決定，見「待你決定」第 2 點）

共用表裡有 FN-DSA，所以兩端一改成從共用表產生對照，就會**同時**認得 -54/-55：

| 地方 | 改完後的行為 | 原本排在哪天 |
|---|---|---|
| authenticator 選演算法（`service.py:323–327`） | RP 的 `pubKeyCredParams` 裡有 -54/-55、而且排在前面時，會選用 FN-DSA | Day 4 |
| RP 登入驗章（`services.py:182`） | DB 裡的憑證若是 -54/-55，可以驗章 | Day 3 |
| RP 註冊（`services.py:118`） | **不變**：仍只接受 `hosted_algorithms` 的 `[-49, -48, -50]`，所以 DB 裡目前不可能出現 FN-DSA 憑證 | Day 3 才加 -54/-55 |
| RP 宣告（`/register/options`） | **不變**：仍只宣告 ML-DSA | Day 3 |

也就是說，在我們自己的 RP 上，今天之後行為完全不變（RP 不宣告、也不接受 FN-DSA 註冊）；只有面對「會宣告 -54/-55 的其他 RP」時，authenticator 會開始選用 FN-DSA。

另外，專案守則要求「共用演算法表裡的每個演算法，都至少要有一個用真的 liboqs 跑『產生金鑰 → 簽章 → RP 驗章』的測試」。FN-DSA 今天進入共用表，所以今天就要有這個測試（T6、T7）。

### 預計修改

| 檔案 | 預計修改 | 對應項目 |
|---|---|---|
| `shared/pq-algorithms.json`（新增） | 五個演算法的共用表 | 1 |
| `shared/__init__.py`、`shared/pq_algorithms.py`（新增） | 讀取與檢查共用表；提供依 COSE 編號查詢的函式 | 2 |
| `shared/tests/test_pq_algorithms.py`（新增） | T1–T5 | 1、2 |
| `authenticator/pqcrypto.py:14–18` | `COSE_ALG_TO_OQS` 改從共用表產生，並補齊 `PQCSignatureSuite` 的註解 | 3 |
| `rp_server/services.py:195–205` | `COSE_TO_OQS` 改從共用表產生，並補齊 `_cose_to_oqs()` 的註解 | 3 |
| `authenticator/tests/test_pqcrypto.py`（新增） | T6、T8 | 3 |
| `rp_server/tests/test_authentication_verify.py` | T7（五個演算法的真實驗章） | 3 |
| `pyproject.toml` | `testpaths` 加入 `shared/tests` | 4 |
| `.github/workflows/ci.yml`、`CLAUDE.md` | ruff 路徑加入 `shared`（`CLAUDE.md` 本身規定新增測試資料夾時要同步更新） | 4 |
| `codex/PROTOCOL-GUIDE.html` 第 11 章 | 名詞表新增「共用演算法表」「COSE 演算法編號（暫定）」等新術語 | 文件 |
| `codex/FN-DSA-PLAN.md` | 勾選 Day 2 | 文件 |

### 測試案例（待你核准）

| 編號 | 情境 | 預期結果 | 依據 | 實作前預期 |
|---|---|---|---|---|
| T1 | 讀入共用表 | 剛好五筆，依序為 -48、-49、-50、-54、-55；每一筆的 `label`、`oqsName`、三個大小、`signatureLengthFixed`、`status` 都等於上面「架構背景 2」的表 | RFC 9964、FIPS 204 Table 2、Falcon v1.2 3.11 節、draft-ietf-cose-falcon-04、liboqs 資料表、D1、D2 | 紅燈（檔案與模組都不存在） |
| T2 | 對共用表的每一筆，向 liboqs 查詢該演算法實際的金鑰與簽章大小（`oqs.Signature(oqsName).details`） | 公鑰、私鑰、簽章大小都和表內相同 | `FN-DSA-PLAN.md` Day 2「表內大小等於 liboqs 實際大小」；確保表和實際使用的函式庫沒有脫節 | 紅燈（模組不存在） |
| T3 | 讀取一份測試用的表：(a) 兩筆的 `coseAlg` 都是 -48；(b) 兩筆的 `oqsName` 都是 `ML-DSA-44` | 都拋出 `ValueError`，訊息指出重複的值 | COSE 演算法編號必須唯一對應一個演算法（IANA COSE Algorithms registry）；`FN-DSA-PLAN.md` Day 2「COSE 編號不重複」 | 紅燈（模組不存在） |
| T4 | 讀取一份測試用的表：(a) 某一筆缺少 `oqsName`；(b) `coseAlg` 是字串 `"-48"`；(c) `status` 是不認得的值 | 都拋出 `ValueError`，訊息指出是哪一筆、哪個欄位 | workflow.md F02 規定的欄位；壞掉的表必須在啟動時就被擋下，不能等到驗章時才出錯 | 紅燈（模組不存在） |
| T5 | 比較 authenticator 的 `COSE_ALG_TO_OQS`、RP 的 `COSE_TO_OQS` 和共用表 | 兩者都等於共用表的「`coseAlg` → `oqsName`」，包含 -54 → `Falcon-512`、-55 → `Falcon-1024` | D3：兩端的對照都只能來自共用表；Day 2 完成標準 | 紅燈（兩端目前只有三筆 ML-DSA） |
| T6 | authenticator 端，對共用表的每個演算法：`PQCSignatureSuite(coseAlg)` 產生金鑰 → 簽一則訊息 → 驗章 | 公鑰、私鑰長度等於表內數值；`signatureLengthFixed` 為真時簽章長度**等於** `signatureBytes`，為假時**不超過** `signatureBytes`；驗章成功 | `CLAUDE.md`「真實密碼學」；FIPS 204（ML-DSA 簽章長度固定）；Falcon v1.2 3.11.6（壓縮格式長度不固定） | -48/-49/-50 綠燈；-54/-55 紅燈（`Unsupported COSE algorithm`） |
| T7 | RP 端，對共用表的每個演算法：用 liboqs 產生金鑰，以該 `coseAlg` 存入 RP 的 DB；對 `authenticatorData ‖ SHA-256(clientDataJSON)` 簽章，送到 `/authenticate/verify` | 回傳 200，驗章成功 | `CLAUDE.md`「真實密碼學」（產生金鑰 → 簽章 → RP 驗章）；WebAuthn §7.2 | -48/-49/-50 綠燈；-54/-55 紅燈（400 `Unsupported algorithm`） |
| T8 | 共用表以外的演算法：`PQCSignatureSuite(-7)`（ES256）；authenticator 收到只有 `[-7]` 的 `pubKeyCredParams` | 前者拋出 `ValueError`（Unsupported COSE algorithm）；後者拋出 `ValueError`（No supported algorithm） | WebAuthn §6.3.2：authenticator 只能從 RP 提供、自己也支援的演算法中選擇，都不支援就必須回錯誤 | 綠燈（回歸保護：確認改用共用表沒有把範圍放寬） |

**破壞檢查**：T3、T5 是今天的關鍵測試。
- T3：拿掉讀取模組裡的重複檢查，確認 T3 變紅。
- T5：把 authenticator 的 `COSE_ALG_TO_OQS` 改回寫死的三筆，確認 T5 變紅（同時 T6 的 -54/-55 也應變紅）。

### 待你決定

1. **Python 讀取模組與測試的位置**：建議放在 `shared/pq_algorithms.py`（`shared/` 同時是 Python 套件），測試放 `shared/tests/`。這需要把 `shared/tests` 加進 `testpaths`、把 `shared` 加進 CI 與 `CLAUDE.md` 的 ruff 路徑。`CLAUDE.md` 本身規定新增測試資料夾時要同步更新，但改 `CLAUDE.md` 仍要經過你同意。
2. **FN-DSA 是否今天就對兩端生效**：建議「是」，也就是共用表的五個演算法都直接生效（見「架構背景 4」）。理由：這正是 Day 2 完成標準要求的「兩端都改從共用表讀取」；在我們自己的 RP 上行為不變；而守則要求的真實密碼學測試（T6、T7）今天就會涵蓋 FN-DSA。另一個選擇是讓讀取模組只開放 ML-DSA、到 Day 3／Day 4 才開放 FN-DSA，但這等於多一個開關，而且 Day 2 的表就沒有被真正用上。

### 待辦清單（中途發現、今天不處理）

- RP 註冊時沒有檢查公鑰長度是否符合演算法（`rp_server/services.py:121–123` 只檢查是 bytes），也沒有檢查 COSE_Key 的 kty（`1`）是否為 7（AKP）。長度錯誤或任意長度的公鑰都會被存進 DB；共用表有 `publicKeyBytes` 之後就能檢查。Day 3 會修改這個函式，可以一併考慮，但要先經過使用者同意。

### 對齊紀錄

- 介紹今日內容後，使用者請 Claude 先說明：為什麼對照表分散會出問題、各個名詞的意思、學長交接文件（`FALCON_INTEGRATION_HANDOVER.md`）的建議做法。Claude 說明分散時的四種錯誤（漏改一層、兩邊翻譯不一致到登入才以 `Invalid signature` 失敗、長度常數錯誤、FIPS 206 遷移時又要改多處），整理名詞表，並對照交接文件 5.1、5.2、第 6 節 Step 2、第 8 節；同時指出三處和交接文件不同：`status` 的意義、新增 `signatureLengthFixed`、交接文件沒有規定的部分（格式、位置、是否立刻生效）。
- 理解確認：使用者回答「分散的話容易漏改，兩邊翻譯不一致驗章就會失敗」。已對上。
- 決定：
  - `status` 採用 Claude 的意義：`standard`／`provisional` 表示 COSE 編號是否已正式分配（依 D1），不採用交接文件的 `stable in repo`／`planned`。
  - FN-DSA 今天就對 RP 與 authenticator 兩端生效（「待你決定」第 2 點採建議做法）。
- 使用者要求列出協議導覽中 RP 與 authenticator 對應的章節以便複習：第 3 章（角色）、第 4 章第 2、5、8 步、第 5 章第 5、8 步、第 6.4、6.5 節、第 7.2 節、第 8.2 節。
- 確認問題：
  - 問題 1（今天生效後，在我們的 RP 註冊會不會選到 FN-DSA）：使用者回答「不會，因為今天還沒加 -54/-55」。Claude 補充完整的因果：RP 的 `hosted_algorithms` 決定 `pubKeyCredParams`，authenticator 只能從這份清單裡挑，清單裡沒有 -54/-55 就不可能選到。已對上。
  - 問題 2（authenticator 寫 `-54 → Falcon-512`、RP 誤寫 `Falcon-1024`）：使用者回答登入時 RP 驗章會出問題，註冊時不知道。Claude 補充：註冊會成功，因為 attestation 格式是 none，註冊時 RP 不驗簽章，也完全不查 liboqs 名稱，只存下編號 -54 和公鑰（導覽第 4 章「為什麼註冊時沒有驗簽章？」）；錯誤要到登入第 8 步才以 `Invalid signature` 出現，那時錯誤的憑證已經存進 DB。這正是 T5 要在測試階段就擋下的情況。
  - 問題 3（752 代表什麼）：使用者回答「簽章大小限制在 752 bytes」。Claude 補充：752 是上限，每次簽章的實際長度都不同（平均約 655）；ML-DSA 每次都剛好 2420 bytes，表裡的數字就是實際長度，所以用 `signatureLengthFixed` 區分兩種意思。T6 因此對 ML-DSA 檢查「等於」，對 FN-DSA 檢查「不超過」。
- 使用者追問問題 2：「註冊時 authenticator 只是照指定的演算法去跑，也不能自己打一些奇怪的東西？」Claude 說明：
  - 問題 2 的錯誤不是 authenticator 亂填，而是開發者把 RP 的表寫錯；兩支程式都誠實照自己的表做事，所以 authenticator 端完全正常。
  - 演算法編號確實不能亂填：RP 在 `rp_server/services.py:118` 檢查編號必須在 `hosted_algorithms` 裡，否則回 400 `Unsupported algorithm`。
  - 但公鑰本身可以亂填：RP 只檢查 `-1` 是 bytes（`services.py:121–123`），不檢查長度是否符合演算法，也不檢查 `1`（kty）是不是 7（AKP）；attestation 為 none，也沒有證明 authenticator 真的持有對應的私鑰。這是既有問題，記入待辦清單。
- 決定：讀取模組放 `shared/pq_algorithms.py`，測試放 `shared/tests/`；同意依 `CLAUDE.md` 的規定，把 `shared/tests` 加進 `testpaths`，把 `shared` 加進 CI 與 `CLAUDE.md` 的 ruff 路徑（「待你決定」第 1 點採建議做法）。
- 測試案例 T1–T8：使用者已於 11/17 核准。
