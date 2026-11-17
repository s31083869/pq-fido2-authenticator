# Day 2：F01 + F02 共用演算法表

| 項目 | 內容 |
|---|---|
| 日期 | 2026-11-17 |
| 分支 | `day-02`（從 `origin/main` 7020c73 開出） |
| 狀態 | 完工：T1–T10、三項輕微修正與 T9 (i) 的加強都已完成，待 PR 的 CI 結果 |

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
- Python authenticator 先要求使用者驗證（Windows Hello，`authenticator/service.py:138`），才檢查演算法（`:153`）。所以 RP 只提供不支援的演算法（例如只有 `[-7]`）時，使用者會先看到 Windows Hello 視窗，之後才被拒絕。WebAuthn §6.3.2 的步驟 2（檢查演算法，不支援就回 NotSupportedError）排在使用者同意與驗證之前。測試用的是 NoopVerifier，看不出這個問題。和 Day 1 待辦中「找不到憑證時先跳 Windows Hello」是同一類問題，可以一起處理。
- T5 比對的是「值相等」，所以某一端改回寫死、但五筆內容都和共用表相同時，T5 抓不到。這是設計極限：寫死但內容錯的情況都抓得到。若要更嚴格，可以另外確認兩端的對照是由 `cose_to_oqs_names()` 產生。
- 讀取模組的測試還有三個缺口（第 2 次獨立審查）：名稱欄位為非字串（例如 `label: 123`）、`"algorithms"` 存在但不是清單，這兩種情況都沒有測試；`_entry()` 的 docstring 沒有提到 T9 也會使用它。
- 協議導覽的 Padded 說明可以補一句：補滿格式（666 bytes）比不補滿格式的上限（752 bytes）小，是因為壓縮結果超過固定長度時會重新簽章。

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

### 追加工作（11/17，依獨立審查）

獨立審查的結論是「沒有必須修正的項目」，但指出兩個缺口：程式裡有檢查，卻沒有測試保護。之後重構時被拿掉，也不會有人發現。另外還有一個小 bug。

1. **讀取模組有 6 項檢查沒有測試保護。** 審查者把它們拿掉，57 個測試仍然全綠：
   - bool 被當成整數接受
   - 未知欄位被接受
   - 大小 ≤ 0 被接受
   - `signatureLengthFixed` 任何型別都接受
   - 空字串的名稱被接受
   - 缺少 `algorithms` 清單

   其中「bool 不當整數」和「多出的欄位」在註解和完工紀錄裡都寫成功能。
2. **小 bug。** `status` 如果是清單這類不能雜湊的值，`value not in VALID_STATUSES` 會丟出 `TypeError`，不是 `ValueError`，和模組說明「都會拋出 ValueError」不一致（`shared/pq_algorithms.py:87`）。
3. **RP 的 `_cose_to_oqs()` 沒有測試保護。** Day 2 改寫了它的註解，寫明「編號不在共用表時回 400」，但審查者把 `abort` 改成退回 ML-DSA-44，全套測試仍綠（`rp_server/services.py:204–213`）。

T9、T10 是新增的測試，T1–T8 的內容不變。除了 T9 (h)，其他實作都已經存在，所以新測試一寫好就會是綠燈，證明它們有效的是破壞檢查（做法同 Day 1 的 T12、T13）。

#### 追加的測試案例（使用者已於 11/17 核准）

| 編號 | 情境 | 預期結果 | 依據 | 實作前預期 |
|---|---|---|---|---|
| T9 | 讀取一份測試用的表，第二筆（索引 1）分別是：(a) `coseAlg` 為 `true`；(b) `publicKeyBytes` 為 `true`；(c) 多出拼錯的欄位 `oqsname`（其他欄位都正確）；(d) `publicKeyBytes` 為 `0`；(e) `signatureLengthFixed` 為字串 `"false"`；(f) `label` 為空字串；(g) `oqsName` 為空字串；(h) `status` 為清單 `["standard"]`；另外 (i) 整份表沒有 `algorithms` 清單 | (a)–(h) 都拋出 `ValueError`，訊息開頭指出 `algorithms[1].<欄位>`；(i) 拋出 `ValueError`，訊息提到 `algorithms` | RFC 8259 §3：JSON 的 `true`／`false` 是獨立的字面值，不是數字；workflow.md F02 規定的欄位；拼錯的欄位若被默默忽略，Python 和之後讀同一份表的 TypeScript 可能看到不同的資料（違反 D3「唯一的資料來源」）；模組說明承諾壞掉的表一律拋出 `ValueError` | (h) 紅燈（目前丟出 `TypeError`）；其他綠燈，有效性由破壞檢查證明 |
| T10 | RP 的 DB 中有一張憑證的演算法是 -7（ES256，不在共用表中），用它送出登入 | `/authenticate/verify` 回傳 400 `Unsupported algorithm`，不嘗試驗章 | WebAuthn §7.2：RP 用註冊時保存的演算法驗章；不認得的演算法無法驗章，必須拒絕，不能改用其他演算法 | 綠燈（回歸保護）；有效性由破壞檢查證明 |

**破壞檢查**：
- T9：依序拿掉 6 項檢查，每次只拿掉一項：整數欄位改用 `isinstance(value, int)`、接受未知欄位、接受大小 ≤ 0、不檢查 `signatureLengthFixed` 的型別、接受空字串名稱、拿掉 `algorithms` 清單的檢查。每次都必須有對應的子情境變紅。
- T10：把 `_cose_to_oqs()` 的 `abort` 改成退回 `ML-DSA-44`，T10 必須變紅。

#### 一併處理的輕微項目（只改註解與文件，不改行為）

- `PQCSignatureSuite.__init__` 補上自己的 docstring（`authenticator/pqcrypto.py:38`）。
- 協議導覽名詞「Padded／unpadded」更正：補滿格式也是先壓縮，再補 0 到固定長度（666／1280）。
- T4 的 docstring：「第 1 筆（索引 1）」改成「索引 1（第二筆）」，避免誤讀。

#### 追加工作的對齊紀錄

- 使用者核准 T9、T10，並同意今天一併修正三項輕微項目（11/17）。
- 第 2 次獨立審查指出 T9 (i) 的斷言 `match="algorithms"` 會比對到暫存檔名，實際上沒有作用。使用者同意加強為 `match=r"'algorithms' list"`（11/17）。這讓測試真的檢查核准的預期「訊息提到 algorithms」，不是改弱。

---

## 完工

### 實際修改

行號以 Day 2 最後一個 commit 的版本為準。

| commit | 檔案:行號 | 改了什麼 | 目的 |
|---|---|---|---|
| `9f6ea0b` | `codex/worklog/day-02.md` | 新增本文件的開工段落 | 在實作前留下測試案例與對齊紀錄 |
| `a56abb7` | `shared/pq-algorithms.json:1–55`（新增） | 五個演算法的共用表，含 `description` 說明欄位意義與數值依據 | F01、F02：唯一的資料來源 |
| `a56abb7` | `shared/__init__.py`（新增） | 讓 `shared/` 成為 Python 套件，說明它放 RP 與 authenticator 共用的定義 | RP 與 authenticator 都能 `import shared` |
| `a56abb7` | `shared/pq_algorithms.py:19–23` | `REGISTRY_PATH`、`VALID_STATUSES` | 表的位置與 status 合法值 |
| `a56abb7` | `shared/pq_algorithms.py:27–62` | `PQAlgorithm`（不可修改的資料物件）與 JSON 欄位對照 `_FIELDS` | 用 Python 慣用的欄位名稱表示一筆演算法 |
| `a56abb7` | `shared/pq_algorithms.py:65–113` | `_check_field()`、`_parse_entry()`：檢查缺欄位、多出的欄位、型別（bool 不當整數）、status | 壞掉的表在啟動時就被擋下 |
| `a56abb7` | `shared/pq_algorithms.py:116–154` | `load_algorithms()`（含 COSE 編號與 liboqs 名稱的重複檢查）、模組載入時的 `ALGORITHMS`、`cose_to_oqs_names()` | 兩端從同一份表取得對照 |
| `a56abb7` | `shared/tests/test_pq_algorithms.py:1–155`（新增，後續 commit 擴充到 215 行） | T1（第 62 行）、T2（第 85 行）、T3（第 115 行）、T4（第 144 行） | 驗證共用表與讀取模組 |
| `a56abb7` | `pyproject.toml:32`、`.github/workflows/ci.yml:50`、`:53`、`CLAUDE.md:83–84` | `testpaths` 加入 `shared/tests`；ruff 路徑加入 `shared` | 依 `CLAUDE.md` 規定同步新增的測試資料夾；CI 也會檢查 |
| `0533723` | `authenticator/pqcrypto.py:10`、`16–20` | `COSE_ALG_TO_OQS` 改由 `cose_to_oqs_names()` 產生 | 不再寫死，和 RP 一致 |
| `0533723` | `authenticator/pqcrypto.py:30–74` | 補齊 `PQCSignatureSuite` 與各方法的註解（邏輯不變；`__init__` 的 docstring 在 `8504318` 補上） | 依守則補註解 |
| `0533723` | `rp_server/services.py:19`、`197–213` | `COSE_TO_OQS` 改由 `cose_to_oqs_names()` 產生，補齊 `_cose_to_oqs()` 的註解 | 不再寫死，和 authenticator 一致 |
| `0533723` | `authenticator/tests/test_pqcrypto.py:1–94`（新增） | T5 authenticator 端（第 19 行）、T6（第 32 行）、T8（第 64、74 行） | 驗證 authenticator 端 |
| `0533723` | `rp_server/tests/test_authentication_verify.py:1–7`、`26–27`、`145–189` | 模組說明更新；T5 RP 端（第 145 行）、T7（第 157 行） | 驗證 RP 端 |
| `7aa0678` | `codex/PROTOCOL-GUIDE.html` 第 8.2、10、11 章 | 新增 `shared/` 目錄卡片、更新測試數、名詞表新增 3 個名詞 | 導覽跟上程式；新術語進名詞表 |
| `f6dcb84` | `codex/worklog/day-02.md` | 開工段落新增「追加工作」（T9、T10、輕微項目與核准紀錄）；完工段落記錄 T1–T8 與獨立審查 | 在寫測試之前留下追加測試案例的核准紀錄 |
| `2dba51e` | `shared/pq_algorithms.py:65–93`（關鍵在第 90 行） | `_check_field()` 檢查 status 前先確認是字串，補齊函式說明 | 清單這類值不再丟出 `TypeError`，壞掉的表一律拋出 `ValueError` |
| `2dba51e` | `shared/tests/test_pq_algorithms.py:157–215` | T9 (a)–(h)（第 193 行）、T9 (i)（第 207 行） | 讀取模組的每一項檢查都有測試保護 |
| `2dba51e` | `rp_server/tests/test_authentication_verify.py:192–215` | T10 | RP 遇到不認得的演算法回 400 的行為有測試保護 |
| `8504318` | `authenticator/pqcrypto.py:38–43`、`codex/PROTOCOL-GUIDE.html:1179`、`shared/tests/test_pq_algorithms.py:151` | `__init__` 補 docstring；更正 Padded／unpadded 的說明；T4 docstring 改為「索引 1（第二筆）」 | 依獨立審查的輕微項目，只改註解與文件 |
| `7f1b2dc` | `shared/tests/test_pq_algorithms.py:207–217` | T9 (i) 的斷言改為比對 `'algorithms' list`，docstring 說明原因 | 依第 2 次獨立審查，讓斷言不會碰巧比對到檔名 |
| 完工紀錄 | `codex/PROTOCOL-GUIDE.html:1108` | Python 測試數改為 67 個 | 導覽跟上最終的測試數 |
| 完工紀錄 | `codex/REPORTS.md` | Decision Log 第 57–59 號 | 記錄今天的三項決定 |
| 完工紀錄 | `codex/FN-DSA-PLAN.md` | 勾選 Day 2 | 讓計畫和實際進度一致 |
| 完工紀錄 | `codex/worklog/day-02.md` | 完工段落 | 本段 |

### 測試結果（實作前 → 實作後）

| 測試 | 實作前 | 實作後 |
|---|---|---|
| T1–T4 | 紅燈：收集階段就失敗，`ModuleNotFoundError: No module named 'shared.pq_algorithms'` | 綠燈（11 個參數化案例） |
| T5 | 紅燈：authenticator 與 RP 兩端都是 `AssertionError`，對照只有 -48/-49/-50 | 綠燈 |
| T6 | ML-DSA 三個綠燈；FN-DSA-512、FN-DSA-1024 紅燈：`ValueError: Unsupported COSE algorithm: -54`（-55 相同） | 綠燈 |
| T7 | ML-DSA 三個綠燈；FN-DSA-512、FN-DSA-1024 紅燈：400 `Unsupported algorithm` | 綠燈 |
| T8 | 綠燈（回歸保護） | 綠燈 |
| T9 (h) | 紅燈：`TypeError: unhashable type: 'list'` | 綠燈 |
| T9 (a)–(g)、(i) | 綠燈（實作已在 `a56abb7`；有效性由破壞檢查證明） | 綠燈 |
| T10 | 綠燈（回歸保護；有效性由破壞檢查證明） | 綠燈 |

T5–T8 寫好、兩端尚未切換時，全套為 6 個失敗、51 個通過，失敗的正是上表預期的 6 個。和開工段落的「實作前預期」完全一致。T9、T10 寫好、尚未修正 status 檢查時，全套為 1 個失敗、66 個通過，失敗的正是 T9 (h)。

整體：Python 測試從 32 個增為 67 個，Extension 11 個、Frontend 4 個。`9f6ea0b`、`a56abb7`、`0533723`、`2dba51e`、`8504318`、`7f1b2dc` commit 前都跑過 8 項必跑檢查並全部通過。`7aa0678`、`f6dcb84` 只改文件，程式和前一個 commit 相同，commit 前沒有重跑；`7aa0678` 由獨立審查補跑，全部通過。

### 破壞檢查

| 測試 | 怎麼改壞 | 結果 |
|---|---|---|
| T3 | 拿掉 `load_algorithms()` 裡兩個重複檢查的 `raise` | T3 的兩個案例都變紅，其他 9 個仍綠 |
| T5 | authenticator 的 `COSE_ALG_TO_OQS` 改回寫死的三筆 ML-DSA | T5（authenticator 端）與 T6 的 FN-DSA-512、FN-DSA-1024 變紅，共 3 個 |
| T5、T7 | RP 的 `COSE_TO_OQS` 把 -54 改對到 `Falcon-1024`（確認問題 2 的情境） | T5（RP 端）與 T7 的 FN-DSA-512 變紅；T7 的錯誤正是 400 `Invalid signature`，和確認問題 2 的說明一致 |
| T9 (a)(b) | 整數欄位改用 `isinstance(value, int)` | 只有 (a)(b) 變紅 |
| T9 (c) | 接受未知欄位 | 只有 (c) 變紅 |
| T9 (d) | 大小欄位接受 ≤ 0 | 只有 (d) 變紅 |
| T9 (e) | 不檢查 `signatureLengthFixed` 的型別 | 只有 (e) 變紅 |
| T9 (f)(g) | 名稱接受空字串 | 只有 (f)(g) 變紅 |
| T9 (i) | 拿掉「必須有 `algorithms` 清單」的檢查 | 只有 (i) 變紅 |
| T9 (i)（`7f1b2dc` 加強斷言後補做） | 錯誤訊息改成 `{path} is malformed`，不再提到 'algorithms' list | 只有 (i) 變紅（加強前這個破壞抓不到） |
| T10 | `_cose_to_oqs()` 遇到不認得的編號改成退回 `ML-DSA-44` | 只有 T10 變紅 |

每次檢查後都已改回正確的實作，並用 SHA-256 確認和破壞前完全相同。

### 獨立審查

**第 1 次（T1–T8，`origin/main..7aa0678`）**：由沒看過實作過程的子代理審查 `origin/main..7aa0678`。它的做法：
- 用 `git worktree` 分別取出 5 個版本，逐一執行 pytest 與 ruff。
- 把新測試放進實作前的版本，重現紅燈。
- 用 29 種方式改壞實作。
- 獨立查證所有預期值。

**結論**：沒有必須修正的項目。
- T1–T8 都忠實對應核准的案例。
- 預期值都來自外部依據：Falcon 的公鑰、私鑰大小，審查者另外用規格的編碼公式算過，結果相同。
- 「實作前預期」（6 紅 51 綠）重現結果一致。
- 每個 commit 單獨取出來都通過。`7aa0678` 由審查者補跑全部 8 項必跑檢查，也都通過。

| 審查意見 | 分類 | 處理 |
|---|---|---|
| 讀取模組有 6 項檢查沒有測試保護（bool 當整數、未知欄位、大小 ≤ 0、`signatureLengthFixed` 型別、空字串名稱、缺 `algorithms` 清單） | 建議 | 使用者核准 T9，已新增並做破壞檢查。commit `2dba51e` |
| `status` 為不能雜湊的值時丟 `TypeError` 而不是 `ValueError` | 建議 | 納入 T9 (h)，先紅後綠修正。commit `2dba51e` |
| RP `_cose_to_oqs()` 遇到未知演算法回 400，這個行為沒有測試 | 建議 | 使用者核准 T10，已新增並做破壞檢查。commit `2dba51e` |
| 演算法檢查排在使用者驗證之後（既有問題） | 建議 | 記入待辦清單 |
| T5 抓不到「寫死但內容完全正確」 | 建議 | 記入待辦清單（設計極限） |
| `7aa0678` commit 前沒有重跑必跑清單 | 輕微 | 工作紀錄已註明；審查者補跑全部通過 |
| `PQCSignatureSuite.__init__` 沒有 docstring | 輕微 | 已修正。commit `8504318` |
| 協議導覽「Padded／unpadded」的寫法會讓人以為補滿格式沒有壓縮 | 輕微 | 已修正。commit `8504318` |
| T4 docstring「第 1 筆（索引 1）」容易誤讀 | 輕微 | 已修正。commit `8504318` |
| T7 單獨抓不到 JSON 的 `oqsName` 寫錯 | 輕微 | 不處理：這類錯誤由 T1、T2 負責 |
| 執行期間不讀 `status`；Falcon 的 AVX2 實作沒有宣稱「不依秘密值分支」 | 輕微（提醒） | 不處理：前者是 REPORTS 第 59 號的決定；後者是 PoC 可接受的風險，Day 11 檢視安全 backlog 時再記錄 |
| 規格「第 3.11.6 節」的節次無法在 repo 內逐字查證 | 輕微 | 不處理：數值已用編碼公式與三處 liboqs 來源交叉確認 |

審查者另外確認沒有問題的項目：
- 從根目錄以 README 的方式啟動 RP 與 authenticator 都能 `import shared`。
- CI 會收集 `shared/tests`，ruff 兩個步驟也都包含 `shared`；`uv.lock` 沒有變動。
- RP 的 `hosted_algorithms` 不變。
- authenticator 只有在 RP 把 -54/-55 列在前面時才會選 FN-DSA。
- 工作紀錄的行號與數字都正確。

**第 2 次（T9、T10，`2dba51e`、`8504318`）**：由另一個沒看過實作過程的子代理審查。
- **結論**：沒有必須修正的項目。T9 (a)–(i)、T10 都忠實對應核准的案例。
- **紅燈重現**：在 `f6dcb84` 上放進新測試，結果是 1 失敗、66 通過，唯一的失敗是 T9 (h) 的 `TypeError`。
- **破壞檢查**：用 12 種方式改壞，核准的 7 項都有對應的測試變紅。
- **逐 commit 驗證**：兩個 commit 單獨取出來都全綠。
- **`8504318`**：拿掉 docstring 後的 AST 和 `2dba51e` 相同，HTML 只改了 1 行，確認只改註解與文件。

| 審查意見 | 分類 | 處理 |
|---|---|---|
| T9 (i) 的 `match="algorithms"` 實際上沒有檢查到東西：錯誤訊息開頭是檔案路徑，暫存檔名 `pq-algorithms.json` 本身就含有 "algorithms"。把訊息改掉，測試仍然全綠 | 建議 | 使用者同意，改為 `match=r"'algorithms' list"`，並補做破壞檢查。commit `7f1b2dc` |
| 名稱欄位只測了空字串，沒有測非字串（`label: 123`） | 輕微 | 記入待辦清單（不在核准範圍內） |
| `"algorithms": {}`（有 key、但不是清單）沒有測試 | 輕微 | 記入待辦清單（不在核准範圍內） |
| `_entry` 的 docstring 只寫「供 T3、T4」，現在 T9 也使用它 | 輕微 | 記入待辦清單（`_entry` 這次沒有修改） |
| T10 靠回應訊息不同，間接證明 RP 沒有嘗試驗章 | 輕微 | 不處理：退回 ML-DSA-44 的破壞會得到 `Invalid signature`，目前抓得到 |
| 導覽的 Padded 說明可以補一句：補滿格式 666 bytes 比不補滿的上限 752 bytes 小，是因為壓縮結果超過固定長度時會重新簽章 | 輕微 | 記入待辦清單，Day 11 同步文件時處理 |
