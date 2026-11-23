# Day 5：Python 路線整合 + 前端選單

| 項目 | 內容 |
|---|---|
| 日期 | 2026-11-23（計畫原訂 11/20；11/19–11/22 沒有進行，計畫日期整體順延 3 天） |
| 分支 | `day-05`（從 `origin/main` d660315 開出） |
| 狀態 | 完工：T1–T6、手動端到端 M1–M3 與依獨立審查的修正都已完成，待 PR 的 CI 結果 |

---

## 開工

### 開工前補記

- Day 4 的 PR #6 三項 CI（Python、Extension、Frontend）都已通過，已於 11/18 合併。`day-04.md` 的狀態欄原本寫「待 PR 的 CI 結果」，今天一併改為已通過。
- 進度：Day 1–4 完成，剩 Day 5–12 共 8 個 Day。照「一天一個 Day」順延，Day 12 落在 11/30，離 2027 年 3 月的期限仍有充足緩衝。`FN-DSA-PLAN.md` 的「日期調整」欄一併更新。

### 今日目標

計畫書的 Day 5 有三項：

| 計畫項目 | 現況 | 今天要做的 |
|---|---|---|
| pytest 整合測試：authenticator ↔ RP 完整註冊 + 登入，五種演算法都跑 | 兩端各自有測試，但從沒有接在一起跑過：authenticator 的輸出直接交給 RP 驗證 | 新增 `tests/integration/`，T1–T3 |
| 前端選單加入 FN-DSA；排序只在 RP 有宣告的演算法中進行 | 選單只有三個 ML-DSA（`frontend/src/pages/index.tsx:101–105`）；排序會把選到的演算法**硬塞**到最前面（`:193–197`），就算 RP 沒宣告也一樣 | 把選單與排序抽成可測的 `frontend/src/lib/algorithms.ts`，T4–T6 |
| 手動端到端：-54、-55 各跑一次註冊 + 登入，檢查 DB 的 `algorithm` | 還沒跑過 | 使用者照清單 M1–M2 親手執行（真的 Windows Hello） |

依序完成，每一項各自一個 commit（訊息格式 `Day 5: …`）：

1. 新增 Python 路線的整合測試：T1–T3（含 `pyproject.toml`、CI、`CLAUDE.md` 的路徑同步）
2. 前端選單與排序：T4–T6
3. 手動端到端 M1–M2，結果記進完工段落

**完成標準**（`FN-DSA-PLAN.md` Day 5）：Python bridge 路線的 FN-DSA 端到端成功（F17 前半）。

### 架構背景

#### 1. Python 路線上，一次註冊經過哪些元件

```
RP（Flask）          前端（Next.js 頁面）             bridge（Playwright）         authenticator（Python）
/register/options ─→ 收到 pubKeyCredParams
                     依選單重排（今天要修） ─→ navigator.credentials.create
                                                   被攔截，轉成 base64url ─→ make_credential()
                                                                             選演算法、產生金鑰、簽 attestation
                     ←──────────────────────── 組回 PublicKeyCredential ←──
/register/verify ←── 把結果送回 RP
檢查 alg 有宣告、kty、公鑰長度，存進 DB
```

Day 2–4 分別測了 RP 與 authenticator，但每一邊都是用**自己做出來的**假資料測另一邊。今天的整合測試把 authenticator 真正的輸出原封不動交給 RP，等於在 pytest 裡重現上圖，只是把「前端 + bridge」換成幾行程式。這一層會抓到「兩邊各自都對，接起來卻不對」的問題，例如欄位名稱或 base64url 編碼不一致。

整合測試不經過瀏覽器，所以 bridge 注入腳本（JavaScript）不在測試範圍內；這部分由手動端到端 M1–M2 覆蓋。

#### 2. 前端排序的 bug

現在的程式（`index.tsx:193–197`）：

```ts
const orderedParams = [
  { type: "public-key", alg: algorithm },                        // 使用者選的，一律放第一個
  ...normalizedParams.filter((param) => param.alg !== algorithm), // RP 給的其他演算法
];
```

選單上選的演算法**不管 RP 有沒有宣告**都會被放進清單。如果 RP 只宣告 ML-DSA，而使用者選了 FN-DSA-512：

1. authenticator 照規則選清單第一個自己支援的 → -54
2. 使用者看到 Windows Hello、驗證完成
3. RP 收到 -54，不在 `hosted_algorithms` 裡 → 回 400（Day 3 的 T3）

結果是使用者白白驗證一次，最後只看到一個 400。Day 4 對齊時說明過：authenticator 只能相信收到的清單，所以這不是 authenticator 的錯，而是前端不該替 RP 增加演算法。

修正後的規則：**只在 RP 的清單裡面調整順序**。選到的演算法在清單裡，就把它移到第一個、其他保持原本的相對順序；不在清單裡，處理方式見「待你決定」第 1 點。

再次提醒誰決定什麼（Day 3 已說明）：

| 角色 | 決定什麼 |
|---|---|
| RP | 接受哪些演算法、偏好順序（`hosted_algorithms`） |
| 前端（RP 自己的網頁） | 只能在 RP 的清單內重排，讓 demo 可以指定要測哪個演算法 |
| authenticator | 從收到的清單裡挑第一個自己支援的 |

#### 3. 為什麼把排序抽到 `lib/algorithms.ts`

排序寫在 React 元件的事件處理函式裡，bun 測試碰不到。抽成一個純函式 `orderPubKeyCredParams(rpParams, preferredAlg)`，元件只負責呼叫它，就能用 bun 直接測。這也符合 TDD：先寫測試、確認紅燈，再實作。

選單清單 `ALGORITHM_OPTIONS` 也放在同一個檔案。它的內容應該和共用表 `shared/pq-algorithms.json` 一致，做法見「待你決定」第 2 點。

#### 4. 整合測試的做法

| 項目 | 做法 | 理由 |
|---|---|---|
| RP | `create_app()` + Flask `test_client()`，DB 放在 pytest 的暫存資料夾 | 不碰 `rp_server/data/`；和 `rp_server/tests/test_app.py` 相同做法 |
| authenticator | 真的 `Authenticator`、真的 liboqs、`NoopVerifier`；keyring 換成記憶體版（和 `authenticator/tests/conftest.py` 相同做法） | `CLAUDE.md`「真實密碼學」；自動化測試不跳 Windows Hello；不碰使用者的 keyring |
| 前端 + bridge | 測試裡用幾行程式代替：把 RP 的回應交給 `make_credential()`，origin 固定 `http://localhost:3000`，再把結果送回 RP | 和 bridge 的 `_handle_make()` 傳給 authenticator 的內容相同 |
| 指定演算法 | 測試自己把目標演算法移到清單第一個（照修正後的前端規則） | Python 測試不能呼叫 TypeScript；前端規則本身由 T5 測 |

### 預計修改

| 檔案 | 預計修改 | 對應項目 |
|---|---|---|
| `tests/integration/conftest.py`（新增） | 記憶體版 keyring、暫存 RP 與 authenticator 的 fixture | 1 |
| `tests/integration/test_python_route.py`（新增） | T1–T3 | 1 |
| `pyproject.toml` | `testpaths` 加入 `tests/integration` | 1 |
| `.github/workflows/ci.yml:50、53` | ruff 路徑加入 `tests` | 1 |
| `CLAUDE.md`「每次 commit 前必須全部通過」 | ruff 兩行加入 `tests`（守則本身要求同步，但改 `CLAUDE.md` 需要你同意，見「待你決定」第 3 點） | 1 |
| `frontend/src/lib/algorithms.ts`（新增） | `ALGORITHM_OPTIONS`、`orderPubKeyCredParams()` | 2 |
| `frontend/src/lib/algorithms.test.ts`（新增） | T4–T6 | 2 |
| `frontend/src/pages/index.tsx:101–105、193–197、343、386` | 改用新模組；說明文字「ML-DSA algorithm」改為「Algorithm」；註冊處理函式補齊註解 | 2 |
| `codex/PROTOCOL-GUIDE.html` | 前端排序規則、測試數、Day 5 進度；新名詞（整合測試）加進第 11 章 | 文件 |
| `codex/worklog/day-04.md:7` | 狀態改為 CI 已通過 | 文件 |
| `codex/FN-DSA-PLAN.md` | 日期順延；勾選 Day 5 | 文件 |

### 測試案例（待你核准）

| 編號 | 情境 | 預期結果 | 依據 | 實作前預期 |
|---|---|---|---|---|
| T1 | 整合、真的 liboqs。RP 預設設定，五個演算法 (a) -48 (b) -49 (c) -50 (d) -54 (e) -55 各跑一次：取 `/register/options`，把目標演算法移到第一個，交給 `make_credential()`，結果送 `/register/verify` | RP 回 200、`success` 為 true；DB 的 `credential` 表裡該使用者剛好一張憑證，`algorithm` 等於目標演算法；`public_key` 欄位解碼後的公鑰長度 (a) 1312 (b) 1952 (c) 2592 (d) 897 (e) 1793 bytes（欄位的編碼方式實作時先讀 `rp_server/services.py` 確認，不跑程式抄值） | workflow.md F14（註冊後保存 `algorithm=-54/-55`）、F17；FIPS 204 Table 2（ML-DSA 公鑰）；Falcon v1.2 第 3.11 節（FN-DSA 公鑰）；WebAuthn §7.1 | 綠燈（兩端 Day 2–4 都已完成；這是第一次接起來跑，若紅燈代表找到介面不一致） |
| T2 | 接著 T1，同一個使用者登入：取 `/authenticate/options`，交給 `get_assertion()`，結果送 `/authenticate/verify` | RP 回 200、`success` 為 true；DB 裡該憑證的 `sign_count` 從 0 變成 1 | workflow.md F15、F17；WebAuthn §7.2（RP 驗章）、§6.1.1（signCount 每次使用遞增） | 綠燈（同上） |
| T3 | 整合、真的 liboqs。RP 的 `hosted_algorithms` 設為 `[-49, -48, -50]`（沒宣告 FN-DSA），但模擬舊前端的 bug：把 -54 塞到清單最前面 | authenticator 選 -54（照收到的清單）；RP 的 `/register/verify` 回 400；DB 裡沒有任何憑證 | workflow.md F16；WebAuthn §7.1（alg 必須是 RP 在 pubKeyCredParams 宣告過的）；Day 4 對齊紀錄「保證要靠兩端」 | 綠燈（回歸保護：證明前端出錯時 RP 仍擋得住） |
| T4 | 前端 bun 測試：讀取 `shared/pq-algorithms.json`，和 `ALGORITHM_OPTIONS` 比對 | `ALGORITHM_OPTIONS` 剛好五筆，`label` 與 `value` 依序等於共用表的 `label` 與 `coseAlg`：ML-DSA-44 -48、ML-DSA-65 -49、ML-DSA-87 -50、FN-DSA-512 -54、FN-DSA-1024 -55 | 決策 D3（共用表是唯一來源，其他層用測試檢查一致）；workflow.md F01 | 紅燈（模組還不存在；選單目前只有三筆） |
| T5 | 前端 bun 測試：RP 清單為預設的 `[-49, -48, -50, -54, -55]`，`preferredAlg` 分別為 (a) -54 (b) -55 (c) -49 (d) -50 | 回傳的 alg 順序：(a) `[-54, -49, -48, -50, -55]` (b) `[-55, -49, -48, -50, -54]` (c) `[-49, -48, -50, -54, -55]`（不變） (d) `[-50, -49, -48, -54, -55]`；每一筆的 `type` 都是 `public-key`；沒有新增或刪除任何一筆 | `FN-DSA-PLAN.md` Day 5「排序只在 RP 有宣告的演算法中進行」；WebAuthn §5.4（清單順序代表偏好，項目由 RP 決定） | 紅燈（模組還不存在） |
| T6 | 前端 bun 測試：RP 清單為 `[-49, -48, -50]`，`preferredAlg` 為 -54（RP 沒宣告） | 依「待你決定」第 1 點：建議做法是拋出錯誤，訊息指出 RP 沒有宣告這個演算法，**不會**回傳含 -54 的清單 | 同 T5；workflow.md F16 | 紅燈（模組還不存在） |

T6 依「待你決定」第 1 點採 (A)：拋出錯誤，訊息包含該演算法的名稱（FN-DSA-512），而且不回傳任何清單；前端在呼叫 `navigator.credentials.create` 之前就停下。

**破壞檢查**：
- T1、T2：整合測試的 origin 改成 `http://localhost:3001`，T1 必須全部變紅（RP 擋下 origin 不符）；RP 驗章前把簽章最後一個 byte 翻轉，T2 必須全部變紅。
- T3：把 RP 的「alg 必須在 `hosted_algorithms`」檢查拿掉，T3 必須變紅。
- T4：在 `ALGORITHM_OPTIONS` 拿掉 FN-DSA-1024，或把 -54 改成 -53，T4 必須變紅。
- T5、T6：把 `orderPubKeyCredParams()` 改回舊的「硬塞到最前面」寫法，T6 必須變紅；改成「選到的移到最後」，T5 必須變紅。

### 手動端到端（使用者親手執行，真的 Windows Hello）

依 `CLAUDE.md`「端到端測試：Python 路線完成時」。開三個終端機，都在專案根目錄：

1. RP：`uv run flask --app rp_server.app run --port 5005 --debug`
2. 前端：`cd frontend; bun run dev`
3. bridge：`uv run python -m authenticator --url http://localhost:3000`

| 編號 | 步驟 | 預期結果 |
|---|---|---|
| M1 | 在 bridge 開出的瀏覽器中，選單選 FN-DSA-512，使用者名稱 `fn512`，按註冊並完成 Windows Hello；接著切到登入分頁，用 `fn512` 登入 | 兩次都出現成功訊息；RP 的 log 顯示註冊的 alg 為 -54 |
| M2 | 同 M1，改選 FN-DSA-1024，使用者名稱 `fn1024` | 同上，alg 為 -55 |
| M3 | 查 DB（只讀，表名與欄位見 `rp_server/models.py:12–29`）：`uv run python -c "import sqlite3; print(sqlite3.connect('file:rp_server/data/rp.db?mode=ro', uri=True).execute('select u.username, c.algorithm, c.sign_count from credential c join user u on u.id = c.user_id').fetchall())"` | `fn512` 的 algorithm 為 -54、`fn1024` 為 -55，sign_count 都是 1 |

M1–M3 會在 `rp_server/data/rp.db` 新增兩個使用者，這是你自己執行 RP 時寫入的，Claude 不會動這個檔案。

### 待你決定（已決定，見對齊紀錄）

1. **選到的演算法 RP 沒宣告時，前端怎麼做**（影響 T6）：
   - (A，建議) 不呼叫 `navigator.credentials.create`，直接顯示錯誤「RP 沒有宣告 FN-DSA-512」。理由：使用者明確指定要測某個演算法，悄悄換成別的會讓 demo 結果誤導人；也不會白白跳出 Windows Hello。
   - (B) 照 RP 原本的順序送出，再提示「改用了 RP 的第一個演算法」。
2. **前端選單從哪裡來**（影響 T4）：
   - (A，建議) 前端自己保留一份清單，由 T4 讀共用表比對，不一致就紅燈。理由：Next.js 要從專案資料夾外 import JSON，得改建置設定，風險高於收益；C bridge（D3）也是用測試檢查一致。
   - (B) 前端直接 import `shared/pq-algorithms.json`，需要修改 Next.js 設定。
3. **是否同意修改 `CLAUDE.md`**：守則寫明「新增 `tests/` 資料夾後，要同步加進 testpaths 與 ruff 路徑」，但改 `CLAUDE.md` 本身要先取得你的同意。只改必跑清單的兩行 ruff 指令，把 `tests` 加到路徑最後。

### 待辦清單（中途發現、今天不處理）

- 前端註冊完成後沒有顯示 authenticator **實際選到**的演算法。authenticator 不支援選單上選的演算法時，會依 WebAuthn §6.3.2 改選清單中下一個支援的，使用者看不出來（例如目前的 Extension 不支援 Falcon）。可以改成讀出回應的 `publicKeyAlgorithm`，顯示在畫面與 log，選單文字改為「優先演算法」。使用者決定先記入待辦（11/23）。
- （獨立審查）沒有任何測試能發現 `frontend/src/pages/index.tsx` 是否真的呼叫 `orderPubKeyCredParams()`：把頁面改回「硬塞」或直接送 RP 原本的清單，前端測試、tsc、lint 都通過。T6 在頁面上的行為（顯示錯誤、不跳出 Windows Hello）也沒有驗證。Day 12 回歸測試的手動清單加一步：RP 的 `hosted_algorithms` 不含 FN-DSA 時，選 FN-DSA 應直接看到錯誤、不跳出 Windows Hello。
- （獨立審查）RP 的 origin 檢查沒有回歸測試：拿掉註冊（`rp_server/services.py:127`）或登入（`:210`）的 origin 檢查，全部 103 個 Python 測試仍通過。Day 5 之前就有的缺口，Day 10「測試補強」處理。
- （獨立審查）`import rp_server.app` 時，模組最後一行的 `app = create_app()` 會以預設設定開啟 `rp_server/data/rp.db` 並建立資料表（只建表、不寫資料列），所以在主 checkout 跑 pytest 會碰到使用者的資料檔。`rp_server/tests` 原本就這樣。Day 10 一併處理（例如改成延遲建立 app）。
- （獨立審查）`orderPubKeyCredParams()` 的「不修改傳入的 rpParams」沒有測試：改成就地排序後 6 個前端測試都通過。Day 10 處理。
- （獨立審查）整合測試直接把 RP 的 user handle 交給 authenticator；真的路線上前端與 bridge 會轉成 base64url(UTF-8(handle))（28 字元）。RP 目前不檢查 userHandle，所以不影響結果。是否在整合測試模擬這個轉換，Day 10 決定。
- 沿用 Day 1–4 的待辦清單。

### 對齊紀錄

- 決定（11/23）：「待你決定」三點都採建議做法。
  1. RP 沒宣告選到的演算法時，前端直接顯示錯誤、不送出請求（T6）。
  2. 前端自己保留選單清單，由 T4 讀共用表比對。
  3. 同意修改 `CLAUDE.md` 必跑清單的兩行 ruff 指令，加入 `tests`。
- 測試案例 T1–T6：使用者已於 11/23 核准。
- 理解確認（第一輪）：
  - 問題 1（RP 預設清單、選 FN-DSA-1024，送出的清單與 authenticator 的選擇）：使用者回答 `[-55, -49, -48, -50, -54]`。清單正確；Claude 補充 authenticator 選 -55，因為它是清單中第一個自己支援的。
  - 問題 2（RP 只宣告 `[-49, -48, -50]`、選 FN-DSA-512，修正前後）：修正前「直接放進清單，先完成 Windows Hello，最後收到 400」，已對上。修正後回答「選取的放到第一個」，有落差。Claude 補充：
    - -54 不在 RP 的清單裡，沒有東西可以移到前面。依決定 1，前端直接顯示錯誤、不送出，也不會跳出 Windows Hello。
    - 規則是「移到第一個、其他保持原本的相對順序」，不是「對調」。
  - 問題 3（T3 中 authenticator 選 -54 為什麼不算錯、誰擋下）：使用者回答「RP」，對上。Claude 補充：authenticator 看不到 RP 原本的清單，只能相信收到的那份，所以照規則選 -54 不算錯。
- 使用者要求在寫程式之前，用圖完整說明 RP 清單、`hosted_algorithms`、選擇判斷與驗證的流程，確認完全理解後才開始實作。Claude 用兩張圖說明（11/23）：
  - 流程圖：`hosted_algorithms` 用在頭尾兩處；三個檢查點（前端、authenticator、RP）各有失敗出口。
  - 互動模擬：可切換 RP 宣告、選單、修正前後，觀察每一步的結果。
- 使用者問「第一個自己支援的」是依什麼決定，並要求定義清楚四份清單。Claude 說明（11/23）：
  - ① `hosted_algorithms`（`rp_server/config.py:42`）：RP 的設定，有順序。用在兩處：產生 ②、在 `/register/verify` 檢查回來的 alg（`rp_server/services.py:151`）。
  - ② RP 的清單（`pubKeyCredParams`，`rp_server/app.py:141`）：由 ① 原樣產生，內容與順序相同。
  - ③ 前端的清單（`frontend/src/pages/index.tsx:193`）：由 ② 重排而來。修正後項目必須和 ② 相同，只有順序可能不同。
  - ④ authenticator 的支援表（`COSE_ALG_TO_OQS`，`authenticator/pqcrypto.py:20`，由共用表產生）：authenticator 自己的能力，沒有順序，只查有沒有。
  - 選擇規則（`authenticator/service.py:328–332`）：依 ③ 的順序逐項查 ④，第一個在 ④ 裡的就選。「第一個」看 ③，「支援」看 ④。
  - Python authenticator 的 ④ 包含全部五個演算法，所以目前總是選 ③ 的第一個。Extension 目前的 ④ 只有 ML-DSA，會跳過 FN-DSA，這要到 Day 6–7 才補上。
  - 用互動模擬說明：四份清單可以分別調整，並可切換 ④ 為 Python 或 Extension 的支援表。
- 理解確認（第二輪）：
  - 問題 1（「第一個」與「支援」各看哪份清單）：使用者回答「③、④」。已對上。
  - 問題 2（① 為 `[-54, -49]`、選 ML-DSA-44，修正後）：使用者回答「不會跳 Windows Hello，直接顯示錯誤並停止」。已對上。
  - 問題 3（前端已經會擋，RP 為什麼還要用 ① 檢查）：使用者回答「不太清楚」。Claude 用圖說明：
    - 到達 `/register/verify` 的路不只一條。被修改的頁面、舊版或有 bug 的前端、直接用 curl 或腳本送出的請求，都不會經過前端的檢查。
    - 前端的檢查是為了使用體驗，可以被繞過；RP 的檢查在伺服器上執行，不能被繞過，是規則本身（WebAuthn §7.1）。
    - 本專案的例子：未來把 -54 從 ① 拿掉時，只靠前端擋，舊版前端或腳本仍能註冊 -54。
- 理解確認（第三輪）：
  - 問題（有人主張「前端會擋了，RP 的 `hosted_algorithms` 檢查可以刪掉」，要怎麼回應）：使用者回答「直接用程式送 HTTP（curl、Python 腳本）會繞過前端，RP 沒有檢查就會得到錯誤的結果」。已對上。
  - Claude 補充：那種情況下簽章驗證仍會通過（公鑰與簽章本身合法），問題是 RP 收下了自己不接受的演算法。這一行檢查決定「該不該收」，不是「簽章對不對」。
- 對齊完成（11/23），開始實作。
- 實作 T1–T3 期間，使用者追問兩點，Claude 說明（11/23）：
  - 「該不該收」與「簽章對不對」：先更正第三輪的說法。attestation 為 `none`，註冊時 RP 不驗簽章，簽章要到登入才驗。RP 註冊時的檢查分兩類：
    - 真偽：challenge、origin、rpIdHash、公鑰格式，密碼學與格式規則就能判斷。
    - 政策：alg 是否在 `hosted_algorithms`，只有 RP 自己知道。
    - 腳本註冊的 -54 憑證，真偽檢查與之後的登入驗章都會通過，只有政策檢查擋得住。
  - 「前端選了 authenticator 不支援的演算法，最後存的卻是別的」：
    - 依 WebAuthn §5.4、§6.3.2、§7.1（CTAP2 相同），RP 列出接受的演算法並排出偏好，authenticator 選第一個自己支援的，RP 檢查回來的 alg 有宣告過。
    - 這樣設計是為了相容各種 authenticator、一次完成協商、方便更換演算法。
    - WebAuthn 沒有「使用者選演算法」。本專案前端的選單是 demo 工具，真正的意思是「優先嘗試」。
    - 使用者感覺到的落差，是 demo 介面沒有顯示實際選到的演算法，不是協議的缺陷。要強制只用 FN-DSA，就把 RP 的 `hosted_algorithms` 設成只有 `[-54, -55]`。

---

## 完工

### 實際修改

行號以 Day 5 最後一個 commit 的版本為準。

| commit | 檔案:行號 | 改了什麼 | 目的 |
|---|---|---|---|
| `a447e29` | `codex/worklog/day-05.md`、`codex/worklog/day-04.md:7`、`codex/FN-DSA-PLAN.md:9` | 開工段落；day-04 狀態補記 PR #6 的 CI 已通過；計畫日期順延 3 天 | 在實作前留下測試案例與對齊紀錄 |
| `59ce57c` | `tests/integration/conftest.py:1–93`（新增，`90f27a6` 修正註解後為 93 行） | 記憶體版 keyring（第 36 行）、真的 authenticator（第 65 行）、可指定 `hosted_algorithms` 的 RP 工廠（第 78 行） | 整合測試的環境：註冊與登入的資料只寫進暫存資料夾，不跳 Windows Hello |
| `59ce57c` | `tests/integration/test_python_route.py:1–204`（新增，`90f27a6` 補註解後為 204 行） | 外部數值表 `ALL_ALGORITHMS`（第 37 行）、模擬前端重排的 `_move_to_front()`（第 58 行）、完整註冊 `_register()`（第 69 行）、T1（第 108 行）、T2（第 135 行）、T3（第 168 行） | F14、F15、F16、F17：authenticator 的真實輸出交給 RP 驗證 |
| `59ce57c` | `pyproject.toml:32–33`、`.github/workflows/ci.yml:50、53`、`CLAUDE.md:83–84` | `testpaths` 加入 `tests/integration`；CI 與必跑清單的 ruff 路徑加入 `tests` | 守則要求新增 `tests/` 時同步；改 `CLAUDE.md` 已取得使用者同意 |
| `59ce57c` | `codex/worklog/day-05.md` | 對齊紀錄補記實作期間的追問；待辦清單 | 文件 |
| `4fb365c` | `frontend/src/lib/algorithms.ts:1–52`（新增） | `PubKeyCredParam` 型別（第 10 行）、`ALGORITHM_OPTIONS`（第 19 行）、`orderPubKeyCredParams()`（第 40 行） | 前端只在 RP 的清單內重排；RP 沒宣告時拋出錯誤 |
| `4fb365c` | `frontend/src/lib/algorithms.test.ts:1–60`（新增，`90f27a6` 加嚴 T6 後為 60 行） | T4（第 25 行）、T5（第 36 行）、T6（第 55 行） | 選單與共用表一致；重排規則 |
| `4fb365c` | `frontend/src/pages/index.tsx:15、86、131、179–261、355、398、407` | 改用新模組（import 第 15 行、型別第 86 行是連動修改），移除「硬塞到最前面」的寫法；選單預設 ML-DSA-65；`handleRegister` 補齊註解；說明文字與選單標籤改為不限 ML-DSA | 修正 Day 5 的排序 bug，選單加入 FN-DSA |
| `2a89d7d` | `codex/PROTOCOL-GUIDE.html` | 第 4 章註冊第 3 步與範例情景、程式碼地圖、第 7 章狀態、第 10 章進度與測試數、第 11 章新增 4 個名詞（hosted_algorithms、演算法協商、整合測試、端到端測試） | 導覽跟上程式 |
| `90f27a6` | `frontend/src/lib/algorithms.test.ts:51–59`、`tests/integration/conftest.py:1–13、37–44`、`tests/integration/test_python_route.py:8–17、82–83、92–96、143–145、173–175`、`frontend/src/pages/index.tsx:129–131、201–204` | 依獨立審查：T6 加嚴為檢查「does not offer FN-DSA-512」；修正 rp.db、keyring、user.id 轉換的說法；寫明 tuple 欄位、T2 的 signCount 依據、T3 對 F16 的解讀；選單預設值改由 `ALGORITHM_OPTIONS` 取得 | 註解與程式一致；T6 符合核准的預期 |
| 完工紀錄 | `codex/REPORTS.md` | Decision Log 第 62 號 | 記錄今天的決定 |
| 完工紀錄 | `codex/FN-DSA-PLAN.md:109–114` | 勾選 Day 5，補上結果 | 讓計畫和實際進度一致 |
| 完工紀錄 | `codex/worklog/day-05.md` | 完工段落 | 本段 |

### 測試結果（實作前 → 實作後）

| 測試 | 實作前 | 實作後 |
|---|---|---|
| T1、T2 | 綠燈（10 個；兩端 Day 2–4 都已完成，第一次接起來跑就通過，沒有發現介面不一致） | 綠燈 |
| T3 | 綠燈（回歸保護） | 綠燈（另加上錯誤訊息檢查，見破壞檢查） |
| T4–T6 | 紅燈：`Cannot find module './algorithms'`（模組還不存在；1 fail、1 error） | 綠燈（6 個） |

T1–T3 的綠燈和開工段落的「實作前預期」一致，有效性由破壞檢查證明。T4–T6 是先寫測試、確認紅燈後才實作。

整體：Python 測試從 92 個增為 103 個，Extension 11 個，前端從 4 個增為 10 個。每個 commit 前都跑過必跑清單並全部通過。

### 破壞檢查

| 測試 | 怎麼改壞 | 結果 |
|---|---|---|
| T1、T2 | 整合測試的 origin 改成 `http://localhost:3001` | T1、T2 共 10 個變紅；T3 原本仍是綠燈（見下一列） |
| T3 | 同上 | 原本 T3 只檢查 400，origin 錯誤也會回 400，所以沒被抓到。T3 加上「錯誤訊息必須是 `Unsupported algorithm`」後，同樣的破壞會讓 T3 變紅。這是加強，沒有放寬已核准的預期值 |
| T2 | RP 驗章前把簽章最後一個 byte 翻轉（`rp_server/services.py:223`） | T2 的 5 個變紅，T1、T3 不受影響 |
| T3 | 拿掉 RP 的 `hosted_algorithms` 檢查 | 只有 T3 變紅 |
| T4 | `ALGORITHM_OPTIONS` 拿掉 FN-DSA-1024 | 只有 T4 變紅 |
| T4 | `ALGORITHM_OPTIONS` 的 -54 改成 -53 | T4 變紅；T6 也變紅（錯誤訊息找不到 FN-DSA-512 這個名稱） |
| T6 | `orderPubKeyCredParams()` 改回舊的「硬塞到最前面」 | 只有 T6 變紅 |
| T5 | `orderPubKeyCredParams()` 改成「選到的移到最後」 | T5 的 4 個變紅 |
| T6（加嚴後） | 錯誤訊息改成只有演算法名稱（`Unknown FN-DSA-512`） | 只有 T6 變紅；加嚴前的 T6 抓不到這種破壞 |

每次檢查後都已改回正確的實作，並用 SHA-256 確認和破壞前完全相同。

### 手動端到端（使用者親手執行，真的 Windows Hello，11/23）

| 編號 | 結果 |
|---|---|
| M1 | 成功。選 FN-DSA-512 註冊並登入；使用者名稱實際用的是 `ccc`（不是清單上的 `fn512`，不影響結果） |
| M2 | 成功。選 FN-DSA-1024，使用者名稱 `fn1024` |
| M3 | Claude 以只讀模式查詢 `rp_server/data/rp.db` 的 FN-DSA 憑證：`[('ccc', -54, 1), ('fn1024', -55, 1)]`，algorithm 與 sign_count 都符合預期 |

F17 前半（Python bridge 路線的 FN-DSA 端到端）完成。

### 獨立審查

由沒看過實作過程的子代理，在獨立的 worktree 審查 `origin/main..2a89d7d`，以開工段落核准的測試案例表為標準。

**結論**：程式與測試沒有需要擋下的問題。T1–T6 都忠實對應核准的案例，預期值都有外部依據；核准的測試案例表在 `a447e29` 之後沒有被改過。

- **紅燈重現**：在 `a447e29` 加入 `algorithms.test.ts`，出現 `Cannot find module './algorithms'`；加入 `tests/integration/` 則是 11 passed，和開工段落的預期一致。
- **預期值查證**：ML-DSA 公鑰用 32 + 320·k（k = 4、6、8）算出 1312、1952、2592；FN-DSA 用 1 + 14n/8 算出 897、1793；T5 四組順序手推正確；WebAuthn 條號與 workflow.md 引用正確。
- **T3 的訊息檢查**：審查者確認是加強。拿掉這一行再把 origin 改錯，T3 仍會通過。
- **破壞檢查**：審查者另外用 35 種方式改壞前端、RP、authenticator、共用表與測試端。沒被任何測試抓到的有：前端就地修改 rpParams（F8）、`index.tsx` 不呼叫新函式（F14、F15）、拿掉 RP 的 origin 檢查（R2、R3），都已記入待辦清單。
- **逐 commit 驗證**：4 個 commit 單獨取出，必跑清單都通過（pytest 92 → 103 → 103 → 103；前端 4 → 4 → 10 → 10）。
- **環境**：審查者沒有安裝或升級任何套件；liboqs 從 `C:\Users\user\_oqs` 載入，沒有觸發下載；沒有修改主 checkout。

| # | 審查意見 | 分類 | 處理 |
|---|---|---|---|
| 1 | 導覽寫了端到端已完成，但紀錄裡沒有 M1–M3 的結果 | 必須修正 | 審查時完工段落還沒 commit；本段已記錄 M1–M3，隨完工紀錄 commit |
| 2 | 缺紅燈結果與破壞檢查的紀錄 | 必須修正 | 同上，見本段「測試結果」「破壞檢查」 |
| 3 | T6 只檢查訊息含「FN-DSA-512」，比核准的「指出 RP 沒有宣告」寬鬆 | 建議 | 使用者同意，改為 `/does not offer FN-DSA-512/`，並做破壞檢查。commit `90f27a6` |
| 4 | 頁面接線沒有任何驗證 | 建議 | 記入待辦清單，Day 12 手動清單加一步 |
| 5 | 整合測試說「和 bridge 傳的內容相同」，但沒有重現 user.id 的轉換 | 建議 | 使用者同意，測試說明改為照實描述差異（`90f27a6`）；是否模擬記入待辦。開工段落架構背景第 4 節的「和 bridge 的 `_handle_make()` 傳給 authenticator 的內容相同」同樣不精確，開工紀錄保留原文，以本段為準 |
| 6 | RP 的 origin 檢查沒有回歸測試 | 建議（既有缺口） | 記入待辦清單，Day 10 |
| 7 | 「不使用 rp_server/data/rp.db」說法不精確，import 時會開啟並建表 | 建議（既有行為） | 使用者同意，conftest 註解改為照實描述（`90f27a6`）；行為本身記入待辦，Day 10 |
| 8 | 「不修改 rpParams」沒有測試 | 建議 | 記入待辦清單，Day 10 |
| 9 | 「私鑰改存記憶體版 keyring」在 Windows 上不成立 | 輕微 | 使用者同意，改為 Windows 上存 DPAPI 檔（暫存資料夾）、CI 上才用記憶體版 keyring（`90f27a6`）。Claude 已核對 `authenticator/storage.py` 的 `_resolve_backend()` |
| 10 | `index.tsx` 註解說 user.id 是 base64url | 輕微 | 使用者同意，已改正（`90f27a6`） |
| 11 | 選單預設值寫死 -49 | 輕微 | 使用者同意，改由 `ALGORITHM_OPTIONS` 取得（`90f27a6`） |
| 12 | `_credentials_of` 沒寫回傳欄位順序 | 輕微 | 使用者同意，docstring 已寫明（`90f27a6`） |
| 13 | 對齊紀錄說 challenge、origin 等「密碼學與格式規則就能判斷」，但 attestation 為 none 時，註冊階段這些欄位沒有密碼學保護，腳本可以任意填入 | 輕微 | 對齊紀錄保留原文，在此更正：註冊時的「真偽檢查」只確認資料符合 RP 這次的 challenge、本站 origin 與 rpId，沒有簽章保護；這也是政策檢查（`hosted_algorithms`）必須由 RP 自己做的原因之一 |
| 14 | T2 的「剛好是 1」不是規格要求 | 輕微 | 使用者同意，T2 docstring 註明來自本專案設計（`90f27a6`） |
| 15 | T3 引用 F16 容易誤讀 | 輕微 | 使用者同意，T3 docstring 寫明本專案對 F16 的解讀（`90f27a6`） |
| 16 | 計畫未勾選；`index.tsx` 有開工文件沒列的連動修改 | 提醒 | 計畫已勾選；連動修改已列在「實際修改」 |

審查者另外確認沒有問題的項目：註解符合守則（`handleRegister` 已補齊）；範圍沒有超出「預計修改」，沒有碰到禁止的資料夾與使用者資料檔，沒有新增依賴；協議導覽與程式一致；開工段落的行號在 `a447e29` 都正確；M1–M3 的指令可用。
