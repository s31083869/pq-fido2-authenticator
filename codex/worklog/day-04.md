# Day 4：F05 + F06 + F16 Python Authenticator 選用 FN-DSA

| 項目 | 內容 |
|---|---|
| 日期 | 2026-11-18（計畫原訂 11/19，Day 3 提前完成，接著開工） |
| 分支 | `day-04`（從 `origin/main` 022674f 開出） |
| 狀態 | 完工：T1–T5 與依獨立審查的修正都已完成；PR #6 的三項 CI 都已通過，11/18 合併 |

---

## 開工

### 開工前補記

- Day 3 的 PR #5 三項 CI（Python、Extension、Frontend）都已通過，已於 11/18 合併。`day-03.md` 的狀態欄原本寫「待 PR 的 CI 結果」，今天一併改為已通過。

### 今日目標

計畫書的 Day 4 有三項。其中第一項在 Day 2 就已完成，所以今天的工作主要是**補測試**，確認 authenticator 真的會照 RP 的清單選擇 FN-DSA。

| 計畫項目 | 現況 | 今天要做的 |
|---|---|---|
| COSE → liboqs 對應改用共用表，-54/-55 可產生金鑰與簽章（F05） | **Day 2 已完成**：`authenticator/pqcrypto.py:20` 由共用表產生；Day 2 的 T6 已直接測過 `PQCSignatureSuite(-54/-55)` | 補一條「經過 `make_credential`／`get_assertion` 完整流程」的真實密碼學測試（T1、T2） |
| 確認 `credentialPublicKey` 為 `{1: 7, 3: -54, -1: 公鑰}`（F06） | 程式本來就是通用的（`authenticator/webauthn.py:18–26`），但只測過 -49 | T1 直接解開 attestationObject 檢查 |
| 選擇結果測試；不支援時拒絕；RP 沒宣告 FN-DSA 時不得選用（F13、F16） | `_select_algorithm()`（`authenticator/service.py:323–327`）的規則正確，但只有 `[-49]` 和 `[-7]` 兩種情況有測試 | T3、T4 |
| 不支援的演算法要在 Windows Hello **之前**就被拒絕（使用者已決定採用） | Day 2 待辦清單第 2 項：目前先跳 Windows Hello，之後才檢查演算法 | T5，並把演算法檢查移到使用者驗證之前 |

依序完成，每一項各自一個 commit（訊息格式 `Day 4: …`）：

1. 新增 FN-DSA 的真實密碼學流程測試：T1、T2
2. 新增演算法選擇測試：T3、T4
3. 註冊時先檢查演算法、再做使用者驗證：T5

**完成標準**（`FN-DSA-PLAN.md` Day 4）：authenticator 嚴格依照 RP 的 `pubKeyCredParams` 選擇演算法。

### 架構背景

#### 1. Python authenticator 註冊時的流程

`make_credential()`（`authenticator/service.py:107–`）目前的順序：

| 順序 | 做什麼 | 程式 |
|---|---|---|
| 1 | 檢查 origin、rpId 和 origin 的網域一致 | `:125–128` |
| 2 | **使用者驗證**（Windows Hello） | `:138` |
| 3 | 檢查 excludeCredentials | `:140–151` |
| 4 | **選演算法**：照清單順序挑第一個自己支援的 | `:153` |
| 5 | 用 liboqs 產生金鑰對，保存私鑰 | `:154–164` |
| 6 | 組 COSE_Key、authenticatorData、attestationObject | `:166–182` |

第 4 步的規則（Day 3 已詳細說明過）：

```python
for param in params:                  # 照 RP（經前端重排後）的順序
    if param.alg in COSE_ALG_TO_OQS:  # 共用表裡有，就是自己支援
        return param.alg
raise ValueError("No supported algorithm from pubKeyCredParams")
```

`COSE_ALG_TO_OQS` 從 Day 2 起就由共用表產生，包含 -54/-55。所以**今天不需要改選擇規則**，要做的是用測試證明它在各種清單下都選對。

#### 2. 「RP 沒宣告 FN-DSA 時不得選用」是怎麼保證的

authenticator 只會從清單**裡面**挑，清單裡沒有 -54/-55，就不可能選到。這和 Day 3 的 T3（RP 端擋下沒宣告的演算法）是同一件事的兩端：

| 端 | 保證 | 測試 |
|---|---|---|
| authenticator | 只從 `pubKeyCredParams` 裡挑，不自己加演算法 | 今天的 T3 (d)(e) |
| RP | 收到沒宣告過的演算法就回 400 | Day 3 的 T3 |

兩端各自擋一次，哪一端出錯，另一端還擋得住。

#### 3. 為什麼演算法檢查應該排在使用者驗證之前（「待你決定」第 1 點）

WebAuthn §6.3.2 authenticatorMakeCredential 的步驟順序是：

1. 檢查參數格式
2. **檢查 `pubKeyCredParams` 裡至少有一個自己支援的演算法，沒有就回 NotSupportedError**
3. 檢查 excludeCredentials
4.–5. 檢查 residentKey、userVerification 等選項
6. **取得使用者同意（使用者驗證）**
7. 用「第一個支援的」演算法產生金鑰

也就是說，演算法不支援時，authenticator 應該**直接拒絕**，不用打擾使用者。我們的程式把順序顛倒了：RP 只給 `[-7]` 時，使用者會先看到 Windows Hello、驗證完才被拒絕。自動化測試用 `NoopVerifier`，所以一直看不出這個問題。

修法只要把 `_select_algorithm()` 那一行移到 `_verify_user()` 之前，選出來的演算法在後面照常使用。excludeCredentials 的檢查位置不動：規格要求遇到重複憑證時先取得使用者同意才回錯誤，避免網站不經使用者同意就能探測裝置上有哪些憑證。

#### 4. 測試的做法

| 測試 | 用真的 liboqs 還是假的簽章器 | 理由 |
|---|---|---|
| T1、T2 | 真的 | `CLAUDE.md`「真實密碼學」；要確認 Falcon 的公鑰長度、簽章真的能驗 |
| T3、T4、T5 | 假的 `FakeSignatureSuite`（`test_authenticator.py` 既有的做法） | 只測「選哪個演算法」的流程，`CLAUDE.md` 允許用假的簽章器測流程；也避免每個案例都產生一次 Falcon 金鑰 |

T5 需要知道「使用者驗證有沒有被呼叫」，所以會寫一個記錄呼叫次數的假 verifier。它和 `NoopVerifier` 一樣不跳出 Windows Hello。

### 預計修改

| 檔案 | 預計修改 | 對應項目 |
|---|---|---|
| `authenticator/tests/test_fn_dsa_flow.py`（新增） | T1、T2 | 1 |
| `authenticator/tests/test_algorithm_selection.py`（新增） | T3、T4、T5；記錄呼叫次數的假 verifier | 2、3 |
| `authenticator/service.py:107–182` | `make_credential()` 先選演算法、再做使用者驗證，並補齊整個函式的註解 | 3 |
| `codex/PROTOCOL-GUIDE.html` 第 4 章第 5 步 | authenticator 內部的步驟順序改成「選演算法 → 使用者驗證 → excludeCredentials」 | 文件 |
| `codex/worklog/day-03.md` | 狀態改為 CI 已通過 | 文件 |
| `codex/FN-DSA-PLAN.md` | 勾選 Day 4 | 文件 |

### 測試案例（待你核准）

| 編號 | 情境 | 預期結果 | 依據 | 實作前預期 |
|---|---|---|---|---|
| T1 | 真的 liboqs，`pubKeyCredParams` 分別為 (a) `[-54]`、(b) `[-55]`，呼叫 `make_credential` | 解開 attestationObject：`credentialPublicKey` 剛好三個欄位 `{1: 7, 3: alg, -1: 公鑰}`，公鑰長度 (a) 897、(b) 1793 bytes；回應的 `publicKeyAlgorithm` 等於 alg；`fmt` 為 `none` | workflow.md F05、F06 驗收標準；RFC 9964（AKP，kty = 7）；Falcon v1.2 第 3.11 節（公鑰 897／1793 bytes） | 綠燈（Day 2 已讓對照包含 FN-DSA；有效性由破壞檢查證明） |
| T2 | 接著用 T1 註冊的憑證呼叫 `get_assertion` | 用 T1 attestation 裡的公鑰，以 liboqs 的 Falcon-512／Falcon-1024 對 `authenticatorData ‖ SHA-256(clientDataJSON)` 驗章成功；簽章長度不超過 (a) 752、(b) 1462 bytes；authenticatorData 的 signCount 為 1 | workflow.md F15；WebAuthn §6.3.3（簽章輸入）；Falcon v1.2 第 3.11.6 節與 liboqs 演算法資料表（不補滿格式的簽章上限）；`CLAUDE.md`「真實密碼學」 | 綠燈（同上） |
| T3 | 假的簽章器，`pubKeyCredParams` 分別為：(a) `[-7, -54]`；(b) `[-49, -48, -50, -54, -55]`（RP 預設）；(c) `[-54, -49]`；(d) `[-49, -48, -50]`（RP 沒宣告 FN-DSA）；(e) `[-48, -55]` | 選到的演算法（`publicKeyAlgorithm`，以及 credentialPublicKey 的 3 欄位）依序為：(a) -54、(b) -49、(c) -54、(d) -49、(e) -48 | WebAuthn §6.3.2：用清單中「第一個自己支援的」演算法；§5.4：清單依 RP 偏好排序；workflow.md F13、F16（RP 沒宣告就不得選用 FN-DSA） | 綠燈（回歸保護；有效性由破壞檢查證明） |
| T4 | 假的簽章器，`pubKeyCredParams` 為 `[-7, -257]`（ES256、RS256，都不在共用表） | 拋出 `ValueError`（No supported algorithm），沒有保存任何憑證 | WebAuthn §6.3.2 第 2 步：都不支援時必須回錯誤，不能自己改用別的演算法；workflow.md F13 | 綠燈（回歸保護；Day 2 的 T8 只測過 `[-7]` 一個） |
| T5 | 假的簽章器、記錄呼叫次數的 verifier：(a) `pubKeyCredParams` 為 `[-7]`；(b) `pubKeyCredParams` 為 `[-54]` | (a) 拋出 `ValueError`（No supported algorithm），使用者驗證**呼叫 0 次**；(b) 註冊成功，使用者驗證**剛好呼叫 1 次** | WebAuthn §6.3.2：第 2 步（演算法檢查）排在第 6 步（取得使用者同意）之前。(b) 確保修改後沒有把使用者驗證弄丟 | (a) 紅燈（目前會先呼叫 1 次）；(b) 綠燈 |

**破壞檢查**：
- T1、T2：把 `authenticator/pqcrypto.py` 的 `COSE_ALG_TO_OQS` 中 -54 改對到 `Falcon-1024`，T1 (a) 的公鑰長度與 T2 (a) 的驗章必須變紅。
- T3：把 `_select_algorithm()` 改成「選清單中最後一個支援的」，以及「忽略清單、一律選 -54」，T3 都必須有案例變紅。
- T4：把 `_select_algorithm()` 改成「都不支援時退回 -49」，T4 必須變紅。
- T5：把演算法檢查移回使用者驗證之後，T5 (a) 必須變紅；拿掉 `_verify_user()` 呼叫，T5 (b) 必須變紅。

### 待你決定（已決定，見對齊紀錄）

1. **註冊時是否把演算法檢查移到使用者驗證之前**（Day 2 待辦清單第 2 項）：建議「是」，加入 T5。使用者採用。
   - 理由：今天的完成標準是「嚴格依照 RP 的 `pubKeyCredParams` 選擇演算法」，而規格的順序就是先檢查演算法、再取得使用者同意。改動只是把一行往前移。
   - 不做的話：今天只做 T1–T4，這一項留在待辦清單。
   - 範圍：只改註冊。登入時「找不到憑證也先跳 Windows Hello」（Day 1 待辦）是同一類問題，但和演算法選擇無關，今天不處理。

### 待辦清單（中途發現、今天不處理）

- `PubKeyCredParam.type` 是 `Literal["public-key"]`（`authenticator/models.py:35`）。清單中只要有一筆 `type` 是其他值，pydantic 就讓整個請求驗證失敗。WebAuthn §5.1.3 的做法是略過不認得的 type、繼續看下一筆。這一步原本由瀏覽器處理，我們的攔截層取代了瀏覽器，所以要由攔截層或 authenticator 負責。目前 RP 只會送 `public-key`，不會觸發。
- （獨立審查）excludeCredentials 必須排在使用者驗證之後，`service.py` 的註解寫明這是刻意的，但沒有任何測試保護：審查者把它移到使用者驗證之前，所有測試都仍是綠燈。可以用 `RecordingVerifier` 補一條「重複憑證時，使用者驗證呼叫 1 次，而且仍然拒絕」。
- （獨立審查）Extension 的 makeCredential 先檢查 excludeCredentials、再做使用者驗證（`extension/src/background/authenticator.ts:234–247`），和 Python 版、WebAuthn §6.3.2 第 3 步不一致。Day 6 修改 Extension 時一併檢視。
- 沿用 Day 1、Day 2、Day 3 的待辦清單。

### 對齊紀錄

- 決定：註冊時把演算法檢查移到使用者驗證之前，加入 T5（「待你決定」第 1 點採建議做法，11/18）。
- 理解確認：
  - 「Day 4 第一項 Day 2 已經做完了」：已對上。
  - 「T1–T4 用破壞檢查證明有效」：已對上。Claude 補充一開始就是綠燈的原因：實作從 Day 2 起就已存在，這幾個測試是驗收和回歸保護。
- 使用者請 Claude 詳細說明順序調整的意思，以及「RP 沒宣告 FN-DSA 時 authenticator 不得選用」靠什麼保證。Claude 說明：
  - 註冊流程的每一步在做什麼。
  - 用三個情境比較改動前後：RP 只給 `[-7]`、RP 給 `[-54]`、重複註冊。只有第一個情境的結果不同：改動後不再跳出 Windows Hello。
  - excludeCredentials 不跟著前移的原因：規格要求遇到重複憑證時先取得使用者同意才回錯誤，避免網站在使用者不知情時探測裝置上有哪些憑證。
  - 選演算法不需要使用者同意，因為它只取決於清單和 authenticator 自己的能力，不會透露裝置上存了哪些憑證。
  - 「不得選用」的保證：
    - authenticator 選出的演算法一定落在「收到的清單」和「自己支援的演算法」的交集裡（`service.py:323–327`）。
    - authenticator 看不到 RP 原本的清單，只能相信收到的那一份。前端把 -54 塞進清單時（Day 5 要修的 bug），authenticator 照規則選它並不算錯。
    - 所以完整的保證要靠兩端：authenticator 不選清單外的演算法（今天的 T3 (d)(e)、T4），RP 擋下沒宣告的演算法（Day 3 的 T3）。
- 確認問題：
  - 問題 1（改動前後，RP 只給 `[-7]` 時會不會跳出 Windows Hello）：使用者回答「改後不會，改前會先跳 Windows Hello」。已對上。
  - 問題 2（`_select_algorithm()` 改成「都不支援就退回 -49」，哪個測試會抓到）：使用者回答「T3？因為不應該選清單中沒有的演算法」。理由對，測試編號有落差。Claude 補充：
    - 抓到的是 **T4**。T3 的五個清單裡都至少有一個支援的演算法，迴圈一定會在中途 return，走不到「都不支援」的分支，所以退回 -49 的破壞對 T3 沒有影響。
    - T4 的清單 `[-7, -257]` 全都不支援，才會走到這個分支：預期拋出 `ValueError`，卻選了 -49，所以變紅。這也是破壞檢查清單裡 T4 那一項。
    - 退回 -49 違反 WebAuthn §6.3.2 第 2 步（都不支援時必須回 NotSupportedError）。-49 不在 RP 給的清單裡，等於 authenticator 替 RP 做了決定。
  - 問題 3（excludeCredentials 為什麼不前移）：使用者回答「不用驗證使用者就能先知道這台裝置有這個憑證」。已對上。Claude 補充：問題在於「網站」能在使用者不知情時探測，所以規格要求先取得使用者同意。
- 測試案例 T1–T5：使用者已於 11/18 核准。
- 獨立審查後，使用者同意一併修正四項只改測試註解的輕微意見（11/18）。

---

## 完工

### 實際修改

行號以 Day 4 最後一個 commit 的版本為準。

| commit | 檔案:行號 | 改了什麼 | 目的 |
|---|---|---|---|
| `c46377f` | `codex/worklog/day-04.md`、`codex/worklog/day-03.md:7` | 新增本文件的開工段落；day-03 狀態補記 PR #5 的 CI 已通過 | 在實作前留下測試案例與對齊紀錄 |
| `db217c3` | `authenticator/tests/test_fn_dsa_flow.py:1–141`（新增，`f1f5acb` 補註解後為 141 行） | 外部數值表 `FN_DSA_CASES`（第 30 行）、解析 authData 的 `_credential_public_key()`（第 56 行）、T1（第 77 行）、T2（第 104 行） | F05、F06、F15：FN-DSA 經過 `make_credential`／`get_assertion` 完整流程的真實密碼學測試 |
| `bd01549` | `authenticator/tests/test_algorithm_selection.py:1–124`（新增，`53b809b`、`f1f5acb` 擴充到 182 行） | `FakeSignatureSuite`（第 28 行）、`_cose_alg_in_attestation()`（第 73 行）、T3（第 99 行）、T4（第 114 行） | F13、F16：選擇規則與「都不支援就拒絕」 |
| `53b809b` | `authenticator/service.py:110–114` | `make_credential()` 說明改為新的步驟順序，並說明依據與 excludeCredentials 不前移的原因 | 依守則補齊修改到的函式的註解 |
| `53b809b` | `authenticator/service.py:139–143` | `_select_algorithm()` 移到 `_verify_user()` 之前 | WebAuthn §6.3.2：演算法不支援時在使用者驗證之前就拒絕 |
| `53b809b` | `authenticator/service.py:144–145`、`158–159` | excludeCredentials 的註解補上「刻意留在使用者驗證之後」；金鑰產生前的註解改為「用前面選定的演算法」 | 讓註解和新順序一致 |
| `53b809b` | `authenticator/tests/test_algorithm_selection.py:127–182` | `RecordingVerifier`（第 127 行）、T5（第 157 行） | 驗證演算法檢查先於使用者驗證，且支援時仍驗證一次 |
| `0df8b01` | `codex/PROTOCOL-GUIDE.html:763`、`799–801`、`1377` | 第 4 章第 5 步與註冊案例 1 的步驟順序；Python 測試數改為 92；補上 Day 4 進度 | 導覽跟上程式 |
| `f1f5acb` | `authenticator/tests/test_algorithm_selection.py`、`test_fn_dsa_flow.py` | 依獨立審查補齊註解（模組說明、方法 docstring、參數表註解位置、T2 用詞）；去掉 docstring 後的 AST 和修改前相同 | 只改註解 |
| 完工紀錄 | `codex/PROTOCOL-GUIDE.html:733` | 時序圖標籤改為「5 · 選演算法、驗證使用者」 | 依獨立審查，讓時序圖和第 763 行一致 |
| 完工紀錄 | `codex/REPORTS.md` | Decision Log 第 61 號 | 記錄今天的決定 |
| 完工紀錄 | `codex/FN-DSA-PLAN.md:103–105` | 勾選 Day 4，註明對照在 Day 2 已完成、另外調整了驗證順序 | 讓計畫和實際進度一致 |
| 完工紀錄 | `codex/worklog/day-04.md` | 完工段落 | 本段 |

協議導覽沒有新增名詞。

### 測試結果（實作前 → 實作後）

| 測試 | 實作前 | 實作後 |
|---|---|---|
| T1、T2 | 綠燈（4 個；Day 2 已讓對照包含 FN-DSA，有效性由破壞檢查證明） | 綠燈 |
| T3、T4 | 綠燈（6 個；回歸保護，有效性由破壞檢查證明） | 綠燈 |
| T5 (a) | 紅燈：`assert 1 == 0`，使用者驗證在演算法檢查之前就被呼叫 | 綠燈 |
| T5 (b) | 綠燈 | 綠燈 |

T1–T4 的綠燈和開工段落的「實作前預期」一致：計畫書 Day 4 的第一項在 Day 2 就已完成，今天的測試是驗收與回歸保護。T5 是先寫測試、確認紅燈後才調整順序。

整體：Python 測試從 80 個增為 92 個，Extension 11 個、Frontend 4 個。6 個 commit（含依審查補註解的 `f1f5acb`）前都跑過 8 項必跑檢查並全部通過。

### 破壞檢查

| 測試 | 怎麼改壞 | 結果 |
|---|---|---|
| T1、T2 | `pqcrypto.py` 的 `COSE_ALG_TO_OQS` 把 -54 改對到 `Falcon-1024` | 只有 T1 (a)、T2 (a) 變紅 |
| T3 | `_select_algorithm()` 改成「選清單中最後一個支援的」 | T3 (b)(c)(d)(e) 變紅；(a) 只有一個支援的演算法，不受影響 |
| T3 | `_select_algorithm()` 改成「忽略清單，一律選 -54」 | T3 (b)(d)(e)、T4 都變紅，連帶 Day 2 的 T8 與其他既有測試共 8 個變紅 |
| T4 | `_select_algorithm()` 改成「都不支援時退回 -49」 | 只有 T4 與 Day 2 的 T8 變紅，T3 全部仍綠（印證確認問題 2 的說明） |
| T5 (a) | 把演算法檢查移回使用者驗證之後 | 只有 T5 (a) 變紅 |
| T5 (b) | 拿掉註冊時的 `_verify_user()` 呼叫 | 只有 T5 (b) 變紅 |

每次檢查後都已改回正確的實作，並用 SHA-256 確認和破壞前完全相同。

### 獨立審查

由沒看過實作過程的子代理審查 `origin/main..0df8b01`，以開工段落核准的測試案例表為標準。

**結論**：沒有必須修正的項目。T1–T5 都忠實對應核准的案例，預期值都來自外部依據。

- **紅燈重現**：在 `c46377f` 放進三個新測試檔，結果是 1 失敗、11 通過。唯一的失敗是 T5 (a) 的 `assert 1 == 0`，和開工段落的「實作前預期」一致。
- **預期值查證**：
  - 公鑰長度用 1 + 14·n/8 算出 897、1793。
  - 簽章上限用 Falcon 參考實作的 `FALCON_SIG_COMPRESSED_MAXSIZE` 公式算出 752、1462。
- **破壞檢查**：用 27 種方式改壞實作，開工清單列的破壞全部被抓到。沒被核准測試抓到的有 3 種：
  - M3／M4：-54／-55 改對到 `Falcon-padded-512`／`Falcon-padded-1024`。兩種格式的金鑰相同，可以互相驗章（`FN-DSA-PLAN.md:43`），所以 T1、T2 抓不到。Day 2 的 T5（對照必須等於共用表）會抓到。
  - M15：excludeCredentials 移到使用者驗證之前。所有測試都抓不到，已記入待辦清單。
  - M16：在原本的呼叫之外再多呼叫一次 `_select_algorithm()`。這種改動不影響結果，不算缺口。
- **逐 commit 驗證**：5 個 commit 單獨取出，pytest（80 → 84 → 90 → 92 → 92）、ruff check、ruff format 都通過。
  - 這個範圍沒有改到 `extension/`、`frontend/`，所以這兩個只在 HEAD 跑一次，也都通過。

| 審查意見 | 分類 | 處理 |
|---|---|---|
| 實作前的紅燈結果要記進工作紀錄 | 建議 | 完工段落「測試結果」已記錄（審查時尚未 commit） |
| 協議導覽時序圖的標籤仍是舊順序「5 · 驗證使用者、選演算法」（`PROTOCOL-GUIDE.html:733`） | 建議 | 已改為「5 · 選演算法、驗證使用者」，隨完工紀錄 commit |
| `test_algorithm_selection.py` 的模組說明只寫「T3、T4」，T5 也在這個檔案 | 輕微 | 使用者同意，已補上。commit `f1f5acb` |
| `FakeSignatureSuite`、`RecordingVerifier` 的方法沒有自己的 docstring | 輕微 | 使用者同意，已補上。commit `f1f5acb` |
| T5 參數表 (b) 的註解被 ruff 擠到 `),` 後面，不好讀 | 輕微 | 使用者同意，註解移到各案例上方。commit `f1f5acb` |
| T2 的說明寫「用 T1 註冊的憑證」，實際上是在 T2 裡自己再註冊一次 | 輕微 | 使用者同意，已更正。commit `f1f5acb` |
| `FakeSignatureSuite` 和 `test_authenticator.py` 既有的寫法重複 | 輕微 | 不處理：測試檔各自獨立比較好讀，不影響正確性 |
| excludeCredentials 必須在使用者驗證之後，目前沒有測試保護 | 建議 | 記入待辦清單（不在核准的 T1–T5 範圍內） |
| Extension 先檢查 excludeCredentials、再做使用者驗證 | 建議 | 記入待辦清單，Day 6 一併檢視 |
| `_select_algorithm()` 的行號在 `53b809b` 之後移到 `:327–332` | 輕微 | 開工段落的 `:323–327` 是開工時的行號，當時正確，保留不改 |

審查者另外確認沒有問題的項目：
- 規格條號（§5.4、§6.3.2 第 2、3、6、7 步、§6.3.3）和註解、工作紀錄的描述一致。
- 順序調整沒有副作用：錯誤型別與 log 不變；拒絕時不寫入儲存層（破壞 M27 證明 T4 的 `list_all() == []` 有效）。
- 修改到的函式註解已補齊。
- 開工段落的行號在 `c46377f` 都正確。
- 協議導覽其他段落（例如第 832 行）仍然正確。
- 範圍沒有超出「預計修改」。
- T5 的測試和實作放在同一個 commit，符合「失敗的測試不 commit」。
