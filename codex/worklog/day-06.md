# Day 6：Extension TypeScript 層（F07–F10）

| 項目 | 內容 |
|---|---|
| 日期 | 2026-11-24（計畫原訂 11/21，已順延） |
| 分支 | `day-06`（從 `origin/main` 42d98eb 開出） |
| 狀態 | 完工：四項實作、破壞檢查與依獨立審查的修正都已完成；尚未 push，待使用者看過審查結果再開 PR |

---

## 開工

### 開工前補記

- Day 5 的 PR #7 三項 CI 都已通過，已於 11/23 合併。`day-05.md` 的狀態欄原本寫「待 PR 的 CI 結果」，今天一併改為已通過。
- **範圍確認（11/24，使用者決定）**：使用者問「既然不用 Yubico 展示 FN-DSA，為什麼 Extension 還要加 FN-DSA，直接用 Playwright 路線就好」。Claude 查證 `codex/REPORTS.md` 第 1–2 節後說明：
  - 當初的順序是先用 Python + Playwright 在 Yubico 上證明可行（原型），再把能力搬到「一般使用者可用」的 Chrome Extension（成品，2026-02-07 決策）。Yubico 是驗證用的網站，不是做 Extension 的理由。
  - 全世界目前沒有公開的 RP 宣告 -54/-55（FIPS 206 未發布、IANA 未分配），所以 FN-DSA 只能用自己的 RP 展示。
  - 展示改為同一個 Extension 跑三個場景：Yubico 上的 ML-DSA（證明能和別人的 RP 互通）、本機 RP 上的 FN-DSA、本機 RP 不宣告 FN-DSA 時不會選它。
  - Extension 路線的簽章由 WASM 版 liboqs 產生、RP 的 Python liboqs 驗章，是兩份分別編譯的實作互相驗證，比 Playwright 路線（兩端同一份 Python liboqs）更有說服力。
  - 使用者決定：**保留 Extension 的 FN-DSA（Day 6–9）**。記入 `codex/REPORTS.md` Decision Log 第 63 條。
- 基準：Extension 測試 11 個（2 個檔案），全部通過。

### 今日目標

計畫書的 Day 6 有三項，對應 workflow.md F07–F10：

| 計畫項目 | 現況 | 今天要做的 |
|---|---|---|
| F07：`SupportedAlg` 型別、設定、options 選單加入 -54/-55 | `messages.ts:1` 只有 `-48 \| -49 \| -50`；`options/App.tsx:131–133` 選單只有三個 ML-DSA | 型別改由支援清單推出；選單從共用表產生 |
| F08：`SUPPORTED_ALGORITHMS`、`toSupportedAlg()`、`selectAlgorithm()` | `authenticator.ts:19` 寫死 `[-48, -49, -50]`，`:34–39` 再寫死一次 | 改用同一份支援清單，T2、T5 |
| F09：COSE_Key 支援 FN-DSA | `credentialPublicKeyCose()`（`:67–75`）已是 `{1: 7, 3: alg, -1: 公鑰}`，結構不用改 | 只補測試確認 -54/-55 的位元組正確，T3 |
| F10：金鑰與簽章長度常數 | `pq-signer.ts:3–19` 三張表寫死 ML-DSA 的大小 | 改從共用表產生；FN-DSA 的簽章長度當上限處理，T1、T4 |

依序完成，每一項各自一個 commit（訊息格式 `Day 6: …`）：

1. 新增 `extension/src/lib/algorithms.ts`，讀共用表：T1
2. 型別、演算法選擇、長度常數改用新模組：T2–T5
3. options 選單從共用表產生
4. 文件（協議導覽、types README）

**完成標準**（`FN-DSA-PLAN.md` Day 6）：TypeScript 型別檢查與 bun 測試通過。

### 架構背景

#### 1. Extension 裡，一次註冊經過哪些元件

```
網頁（RP 的前端）        injected script          content script        background（service worker）
navigator.credentials
  .create(options) ─→   攔截，轉成可序列化格式 ─→ 轉送 ─→              isTrustedSender() 檢查來源
                                                                        PQAuthenticator.makeCredential()
                                                                          selectAlgorithm()      ← 今天改
                                                                          signer.generateKeyPair()（WASM）
                                                                          credentialPublicKeyCose()
                                                                          存進 chrome.storage
  ←──────────────── 組回 PublicKeyCredential ←───────────────────────── 回傳
```

今天只動 background 的「選演算法」與「大小常數」，再加上 options 頁的選單。injected / content script 只是轉送，不看 alg，不用改。

#### 2. 今天做完後，Extension 能做到哪裡

| 階段 | 選得到 FN-DSA？ | 算得出 Falcon 簽章？ | 攔截得到本機 RP？ |
|---|---|---|---|
| 現在 | 否（不在支援清單） | 否 | 否 |
| Day 6 完成 | **是** | 否（WASM 還沒有 Falcon，`pq_bridge.c` 會回錯誤） | 否 |
| Day 7 完成 | 是 | **是** | 否 |
| Day 8 完成 | 是 | 是 | **是** |

所以今天的成果只能用 bun 單元測試驗證，測試裡用假的簽章器（`TestSigner`）。`CLAUDE.md`「真實密碼學」要求的「真的 liboqs 產生金鑰 → 簽章 → RP 驗章」，Python 端 Day 2–5 已經滿足；Extension 端要等 Day 7 有了 Falcon WASM 才能補。

Day 6 之後到 Day 7 之前有一個過渡狀態：如果 RP 把 FN-DSA 排在 ML-DSA 前面，Extension 會選 FN-DSA，然後在產生金鑰時失敗。目前 Extension 只攔截 demo.yubico.com，而它不宣告 FN-DSA，所以實際上不會發生。

#### 3. 支援清單從哪裡來

決策 D3：共用表 `shared/pq-algorithms.json` 是唯一來源。Extension 的做法見「待你決定」第 1 點。

TypeScript 的型別有一個限制：從 JSON 讀進來的 `coseAlg` 型別只是 `number`，推不出 `-48 | -49 | -50 | -54 | -55` 這種字面值型別。所以「型別」仍要在程式裡寫一份清單 `[-48, -49, -50, -54, -55] as const`，再由 T1 檢查它和共用表一致；「大小」則直接從共用表讀。

#### 4. FN-DSA 的簽章長度不固定

Falcon 第三輪規格 v1.2 第 3.11.6 節的不補滿格式（決策 D2），簽章長度每次都不同，只有上限：FN-DSA-512 最多 752 bytes，FN-DSA-1024 最多 1462 bytes（共用表 `signatureLengthFixed: false`）。

| 位置 | 怎麼處理 |
|---|---|
| WASM bridge 的 `sign()`（`liboqs-wasm-bridge.ts:163–202`） | 先配置上限大小的緩衝區，再依 C 函式回傳的實際長度切出簽章。已經寫好，今天不用改 |
| `SIGNATURE_BYTES` 常數 | 對 FN-DSA 代表上限，不是固定長度；註解寫清楚 |
| authenticator 的 `getAssertion()` | 簽章器回傳多長就原封不動放進回應，不補長、不截斷。T4 確認 |
| 測試的 `TestSigner` | 目前一律回傳 `SIGNATURE_BYTES` 長度的假簽章；FN-DSA 改回傳比上限短的長度，才測得出「不補長」 |

#### 5. COSE_Key 的位元組怎麼來（T3 的依據）

`credentialPublicKey` 是 CBOR 編碼的 COSE_Key `{1: 7, 3: alg, -1: 公鑰}`（RFC 9964：kty 7 為 AKP）。依 RFC 8949 第 3.1 節的編碼規則，FN-DSA-512 的開頭 10 個 bytes 可以手算出來：

| bytes | 意義 | 推導 |
|---|---|---|
| `A3` | 有 3 組鍵值的 map | major type 5，數量 3 |
| `01 07` | 鍵 1（kty）= 7 | 小於 24 的正整數直接放在一個 byte |
| `03 38 35` | 鍵 3（alg）= -54 | 負整數是 major type 1，值為 -1 - (-54) = 53 = 0x35；53 ≥ 24，所以用 `0x38` 加一個 byte |
| `20` | 鍵 -1（公鑰） | major type 1，值 0 |
| `59 03 81` | 897 bytes 的 byte string | major type 2；897 = 0x0381 ≥ 256，所以用 `0x59` 加兩個 bytes |

FN-DSA-1024：alg -55 → `38 36`（值 54），公鑰 1793 bytes → `59 07 01`。

在 authData 裡的位置（WebAuthn §6.1）：rpIdHash 32 + flags 1 + signCount 4 + AAGUID 16 + credentialId 長度 2（大端序）+ credentialId，之後就是 COSE_Key。

這些預期值來自 RFC 與 WebAuthn 規格，不是跑程式抄出來的；也不用 Extension 自己的 `encodeCbor()` 產生預期值，避免拿被測的編碼器驗證它自己。

### 預計修改

| 檔案 | 預計修改 | 對應項目 |
|---|---|---|
| `extension/src/lib/algorithms.ts`（新增） | `SUPPORTED_ALGORITHMS`（`as const` 清單）、`SupportedAlg` 型別、`isSupportedAlg()`、從共用表取得 label 與大小 | 1 |
| `extension/src/lib/algorithms.test.ts`（新增） | T1 | 1 |
| `extension/tsconfig.json` | 加 `resolveJsonModule: true`（只在「待你決定」第 1 點採 A 時） | 1 |
| `extension/src/types/messages.ts:1` | `SupportedAlg` 改從新模組匯入後再匯出，既有的 import 不用改 | 2 |
| `extension/src/background/pq-signer.ts:3–19` | 三張大小表改由共用表產生；註明 FN-DSA 的簽章大小是上限 | 2 |
| `extension/src/background/authenticator.ts:19、34–56` | 刪掉寫死的支援清單，改用新模組；補齊這兩個函式的註解 | 2 |
| `extension/src/background/authenticator.test.ts` | `TestSigner` 的型別改為 `SupportedAlg`，FN-DSA 回傳不固定長度的假簽章；新增 T2–T5 | 2 |
| `extension/src/options/App.tsx:131–133` | 選單改由共用表產生 | 3 |
| `extension/src/types/README.md:17` | `SupportedAlg` 的說明加上 -54/-55 | 4 |
| `codex/PROTOCOL-GUIDE.html` | Day 6 進度、測試數；新名詞加進第 11 章 | 4 |
| `codex/REPORTS.md` | Decision Log 第 63 條（保留 Extension 的 FN-DSA） | 開工 |
| `codex/worklog/day-05.md:7` | 狀態改為 CI 已通過、已合併 | 開工 |
| `codex/FN-DSA-PLAN.md` | 勾選 Day 6 | 完工 |

### 測試案例（已核准）

全部是 Extension 的 bun 測試，用假的簽章器 `TestSigner`（原因見架構背景第 2 點）。

| 編號 | 情境 | 預期結果 | 依據 | 實作前預期 |
|---|---|---|---|---|
| T1 | 讀取 `shared/pq-algorithms.json`，和 `extension/src/lib/algorithms.ts` 比對 | `SUPPORTED_ALGORITHMS` 依序等於共用表的 `coseAlg`：`[-48, -49, -50, -54, -55]`；`PUBLIC_KEY_BYTES`、`PRIVATE_KEY_BYTES`、`SIGNATURE_BYTES` 五筆都等於共用表；其中 -54 為 897／1281／752，-55 為 1793／2305／1462 | 決策 D3；Falcon v1.2 第 3.11 節（FN-DSA 大小）；FIPS 204 Table 2（ML-DSA 大小）；workflow.md F10 | 紅燈（模組還不存在） |
| T2 | 註冊，`pubKeyCredParams` 分別為 (a) `[-7, -54]` (b) `[-55]` (c) `[-7, -55, -54]` (d) `[-49, -54]` | 選到的演算法：(a) -54 (b) -55 (c) -55 (d) -49。三處都要一致：回應的 `publicKeyAlgorithm`、`TestSigner.generateKeyPair` 收到的 alg、`chrome.storage` 存的 `algorithm` | workflow.md F08（`[-7,-54]` 選 -54）、F13、F14（storage 保存 `algorithm`）；WebAuthn §6.3.2 第 2 步（依清單順序，選第一個支援的） | (a)–(c) 紅燈（-54/-55 不在支援清單，會丟 `NotSupportedError`）；(d) 綠燈 |
| T3 | 註冊，`pubKeyCredParams` 分別為 (a) `[-54]` (b) `[-55]`；從回應的 `authenticatorData` 依 WebAuthn §6.1 的位置取出 COSE_Key | (a) 開頭 10 bytes 為 `A3 01 07 03 38 35 20 59 03 81`；(b) 為 `A3 01 07 03 38 36 20 59 07 01`。接著的公鑰 bytes 等於回應的 `publicKey`，長度分別為 897、1793；公鑰之後沒有其他資料 | workflow.md F09（`credentialPublicKey[3] === -54/-55`）；RFC 9964（AKP，kty 7）；RFC 8949 第 3.1 節；WebAuthn §6.1 與 Attested Credential Data 一節；推導見架構背景第 5 點 | 紅燈（註冊在選演算法時就失敗） |
| T4 | (a) 用 `[-54]` 註冊後登入，`TestSigner` 對 -54 回傳 650 bytes 的假簽章 (b) 用 `[-55]` 註冊後登入，回傳 1300 bytes | `TestSigner.sign` 收到的 alg 為 (a) -54 (b) -55，私鑰長度為 (a) 1281 (b) 2305；回應的 `signature` 和簽章器回傳的完全相同（長度 650、1300，不補到上限）；`signCount` 為 1 | workflow.md F10、F15；Falcon v1.2 第 3.11.6 節（不補滿格式，長度不固定）；共用表 `signatureLengthFixed: false`；WebAuthn §6.1.1（signCount 遞增） | 紅燈（註冊就失敗） |
| T5 | 設定的 `defaultAlgorithm` 為 -54：(a) `pubKeyCredParams` 為 `[-49, -48, -50]`（RP 沒宣告 FN-DSA） (b) `[-7, -257]`（沒有任何 PQ 演算法） | (a) 選 -49，不是 -54；(b) 丟出 `NotSupportedError`，而且 `generateKeyPair` 一次都沒被呼叫（不產生金鑰、不存任何憑證） | workflow.md F16（RP 未宣告時不可選 FN-DSA）；WebAuthn §6.3.2 第 2 步（都不支援時回 `NotSupportedError`） | 綠燈（回歸保護：證明加入 FN-DSA 後，設定的預設值不會讓 Extension 私自選 FN-DSA） |

既有的 11 個測試保留不動，只把 `TestSigner` 的參數型別從 `-48 | -49 | -50` 改成 `SupportedAlg`，ML-DSA 的假簽章長度維持不變。

**破壞檢查**：
- T1：把共用表的 -54 公鑰大小改成 896（只在測試執行期間），或在 `SUPPORTED_ALGORITHMS` 拿掉 -55，T1 必須變紅。
- T2：把 `selectAlgorithm()` 改成「選清單中最後一個支援的」，T2 (c)、(d) 必須變紅。
- T3：把 `credentialPublicKeyCose()` 的 kty 改成 1，或公鑰少放一個 byte，T3 必須變紅。
- T4：把 `getAssertion()` 回傳的簽章補零到 `SIGNATURE_BYTES` 的長度，T4 必須變紅。
- T5：把 `selectAlgorithm()` 改成「清單裡都不支援時改用 `defaultAlgorithm`」，T5 (b) 必須變紅；改成「`defaultAlgorithm` 有支援就優先選它」，T5 (a) 必須變紅。

options 選單（第 3 項）是 React 畫面，bun 測試碰不到；資料來源由 T1 保證，畫面本身由 `bun run typecheck` 與 Day 9 的手動端到端確認（在設定頁看得到五個選項）。

### 待你決定（已決定，見對齊紀錄）

1. **Extension 怎麼讀共用表**（影響 T1、`tsconfig.json`）：
   - (A，建議) 大小與 label 直接 `import` `shared/pq-algorithms.json`；型別用的 `as const` 清單仍寫在程式裡，由 T1 比對。需要在 `extension/tsconfig.json` 加 `resolveJsonModule: true`。Vite 與 bun 本來就能 import JSON，`vite.config.ts` 不用改，也不用新增套件。理由：D3 本來就寫「Python 與 TypeScript 讀同一份」，前端 Day 5 沒這樣做是因為要改 Next.js 的建置設定，Extension 沒有這個問題；大小只寫在一個地方，以後換成 FIPS 206 只要改共用表。
   - (B) 跟前端 Day 5 一樣，全部寫在程式裡，由 T1 比對共用表。不用改 `tsconfig.json`，但大小會寫兩份。
2. **設定頁的「Default algorithm」實際上沒有作用**：`selectAlgorithm()` 只在 `pubKeyCredParams` 是空的時候才用它（`authenticator.ts:45–47`），但 `makeCredential()` 在更前面（`:226`）就已經擋掉空清單，所以這段永遠不會執行。另外依 WebAuthn §5.1.3（Create a New Credential），清單是空的時候，瀏覽器端應該補上 ES256 與 RS256，而不是改用設定值。
   - (A，建議) 照計畫把 -54/-55 加進選單，今天不改行為；「預設值沒有作用」記到待辦清單，Day 10 或 Day 11 決定要刪掉這個設定還是改文字。理由：只改當天任務需要的地方（`CLAUDE.md`「範圍與禁止事項」）。
   - (B) 今天就刪掉這個設定與選單。

### 待辦清單（中途發現、今天不處理）

- 設定頁的 `defaultAlgorithm` 沒有作用（見「待你決定」第 2 點）。
- Day 6 完成到 Day 7 完成之間，RP 若把 FN-DSA 排在前面，Extension 會選 FN-DSA 再於產生金鑰時失敗（架構背景第 2 點）。目前只攔截 demo.yubico.com，不會發生；Day 7 完成後自然消失。
- （獨立審查）`extension/README.md:13` 仍寫只支援 ML-DSA；另外要註明 Extension 會 import 資料夾外的 `shared/pq-algorithms.json`，建置時需要整個 repo。Day 11 文件同步處理。
- （獨立審查）Day 4、Day 5 的工作紀錄與程式註解也把「依清單順序選第一個支援的」寫成 WebAuthn §6.3.2 第 2 步，正確應為 Level 2 第 7 步。Day 11 文件同步時一併修正。
- 根目錄 `README.md` 的「快速開始」只寫 Playwright 路線，沒有說明 Extension 才是成品、兩條路線各自的定位。Day 11 文件同步（F18）時補上。
- 沿用 Day 1–5 的待辦清單。

### 對齊紀錄

- 待你決定（11/24）：第 1 點採 (A)，Extension 直接 import 共用表，`tsconfig.json` 加 `resolveJsonModule`；第 2 點採 (A)，今天只把 -54/-55 加進選單，`defaultAlgorithm` 沒有作用的問題記入待辦。
- 使用者提問：Extension 在這個專案裡到底做什麼？Playwright 和 Extension 差在哪裡，哪個才是主要內容？（Claude 的說明見下一條）

- Claude 說明（11/24）：兩條路線都是「攔截 `navigator.credentials`、改用自己的 PQ 實作回應」的軟體 authenticator，因為 Chrome 內建的 WebAuthn 只找得到 Windows Hello、安全金鑰這類真的 authenticator，它們都不支援 ML-DSA／FN-DSA。差別在攔截方式與密碼學在哪裡執行：Playwright 路線由 Python 開一個受控制的 Chromium、注入腳本、透過 `expose_binding` 呼叫 Python authenticator（原生 liboqs 0.14.0、私鑰用 DPAPI 加密存檔、直接跳 Windows Hello）；Extension 路線裝在使用者自己的 Chrome，全程留在瀏覽器裡（WASM 版 liboqs、私鑰存 `chrome.storage.local`、預設 `soft-auto` 不做使用者驗證，要另裝 native host 才有 Windows Hello）。依 `REPORTS.md` 第 1–2 節與 `ARCHITECTURE_EXPLAINED.md` 概述，Extension 是成品，Playwright 路線是原型兼開發測試工具，也可當 Extension 的參考實作。

- 使用者說明今天的內容（11/24）：「今天把三處寫死的清單改成讀共用表，加入 -54/-55」。方向正確；以確認問題檢查細節（過渡狀態、簽章長度、測試預期值的來源）。

- 確認問題：
  - 問題 1（Day 6 完成、Day 7 之前，在 demo.yubico.com 註冊會選哪個）：使用者回答「選 ML-DSA，Yubico 沒宣告 FN-DSA」。已對上。Claude 補充：選的是 Yubico 清單中第一個 Extension 支援的 ML-DSA；Extension 只會從 RP 的清單裡挑，自己支援 FN-DSA 也不會主動加進去（F16、T5）。
  - 問題 2（T4 的假簽章為什麼故意比上限 752 短）：使用者表示不清楚。Claude 補充說明（見下一條）。
  - 問題 3（T3 為什麼不用 `encodeCbor()` 產生預期值）：使用者表示不清楚。Claude 補充說明（見下一條）。

- Claude 補充（11/24）：
  - 問題 2：FN-DSA 的簽章長度不固定，752 只是上限。T4 要抓的錯誤是「把簽章補零到 `SIGNATURE_BYTES`」：若假簽章剛好 752 bytes，正確實作與補零實作都輸出 752，測試分不出來；用 650 bytes 時，正確實作輸出 650、補零實作輸出 752，測試才抓得到。真實的 Falcon 簽章也大多短於上限。
  - 問題 3：`encodeCbor()` 本身就是被測的程式，用它產生預期值等於考生自己出答案。例：若它把 -54 誤編成 `38 36`，用它產生的預期值也是 `38 36`，測試照樣通過；依 RFC 8949 手算的 `38 35` 才會讓測試失敗。這個 bug 若漏掉，RP 會把 alg 讀成 -55，註冊被拒。對應 `CLAUDE.md`「避免球員兼裁判」第 2 條。

- 使用者重述（11/24）：問題 2「比上限短才分得出補零 bug」；問題 3「避免球員兼裁判」。兩題都已對上。

- 使用者核准測試案例 T1–T5（11/24）。

---

## 完工

### 實際修改

| 檔案:行號範圍 | 改了什麼 | 目的 | commit |
|---|---|---|---|
| `extension/src/lib/algorithms.ts:1–84`（新增） | `SUPPORTED_ALGORITHMS`（`[-48, -49, -50, -54, -55] as const`）、由它推出的 `SupportedAlg`、`isSupportedAlg()`；`PUBLIC_KEY_BYTES`、`PRIVATE_KEY_BYTES`、`SIGNATURE_BYTES` 直接由 `shared/pq-algorithms.json` 產生；`ALGORITHM_OPTIONS` | F07、F08、F10；決策 D3（共用表是唯一來源）；「待你決定」第 1 點採 A | `47f3753` |
| `extension/src/lib/algorithms.test.ts:1–84`（新增） | T1：支援清單、三張大小表、選單選項比對共用表；大小另外比對規格書數值；`pq-signer.ts` 轉出的必須是同一份表 | T1 | `47f3753` |
| `extension/tsconfig.json:10` | 加 `resolveJsonModule: true` | 讓 TypeScript 接受 import JSON；Vite 與 bun 本來就支援，`vite.config.ts` 不用改 | `47f3753` |
| `extension/src/background/pq-signer.ts:3–5` | 三張寫死的 ML-DSA 大小表改為轉出 `@/lib/algorithms` 的表 | F10；既有的 import 路徑不變 | `47f3753` |
| `extension/src/types/messages.ts:1–5` | `SupportedAlg` 改從 `@/lib/algorithms` 匯入再轉出 | F07；型別與支援清單只寫一次 | `522553d` |
| `extension/src/background/authenticator.ts:1、34–64` | 刪掉寫死的 `SUPPORTED_ALGORITHMS` 與 `toSupportedAlg()`，`selectAlgorithm()` 改用 `isSupportedAlg()`；補齊函式註解（含 defaultAlgorithm 實際上用不到的說明） | F08 | `522553d` |
| `extension/src/background/authenticator.ts:75–92` | `credentialPublicKeyCose()` 補齊註解：ML-DSA 與 FN-DSA 都用 AKP，結構不變；程式邏輯沒改 | F09 | `522553d` |
| `extension/src/background/authenticator.test.ts:4–17、35–97` | `TestSigner` 參數型別改為 `SupportedAlg`，記錄 `generateKeyPair`／`sign` 的呼叫；FN-DSA 回傳比上限短的假簽章（650／1300 bytes）；新增 `extractCredentialPublicKey()` | T2–T5 需要的測試工具；ML-DSA 的假簽章長度不變 | `522553d` |
| `extension/src/background/authenticator.test.ts:249–340` | T2–T5 | T2–T5 | `522553d` |
| `extension/src/options/App.tsx:2、33–150` | 選單改由 `ALGORITHM_OPTIONS` 產生（加入 FN-DSA-512、FN-DSA-1024）；補齊 `App()` 的註解 | F07；「待你決定」第 2 點採 A，不改行為 | `3df88e8` |
| `extension/src/types/README.md:17` | `SupportedAlg` 的說明加入 -54/-55 | 文件 | `1bdf87d` |
| `codex/PROTOCOL-GUIDE.html` | 第 8 章程式碼地圖加入 `extension/src/lib/algorithms.ts`；第 10 章 Day 6 進度與 Extension 測試數；第 11 章新增 Major type、Options page，共用演算法表的說明加入 Extension | 文件 | `1bdf87d` |
| `codex/REPORTS.md`、`codex/worklog/day-05.md:7`、本檔開工段落 | Decision Log 第 63 條；Day 5 狀態改為已合併 | 文件 | `bd2790e` |

和計畫的差異：`pq-signer.ts` 改為轉出共用表，原本排在第 2 項，實際提前到第 1 項。因為 T1 要檢查「`pq-signer.ts` 轉出的就是共用表產生的那份」，兩者必須同一個 commit 才會綠燈。

### 測試結果（實作前 → 實作後）

| 階段 | 結果 |
|---|---|
| 基準（開工時） | Extension 11 個測試全部通過 |
| T1 實作前 | 紅燈：`Cannot find module './algorithms'`（0 pass、1 fail、1 error），與開工文件預期一致 |
| T1 實作後 | Extension 20 個全部通過（T1 共 9 個） |
| T2–T5 實作前 | 23 pass、7 fail。失敗的是 T2 (a)(b)(c)、T3 兩個、T4 兩個，7 個都是 `NotSupportedError: No supported algorithm in pubKeyCredParams`；T2 (d)、T5 (a)(b) 通過。與開工文件的預期一致 |
| T2–T5 實作後 | Extension 30 個全部通過 |
| 最終（每次 commit 前） | Python 103 個、Extension 30 個、前端 10 個全部通過；ruff check、ruff format、Extension typecheck、前端 lint 與 tsc 都通過 |
| 打包 | `vite build` 輸出到 scratchpad（不動 `extension/dist`）成功；共用表被打包進共用的 chunk，設定頁與 background 都會載入 |

### 破壞檢查

每次只改壞一處，跑 `bun test src`，再還原（還原後與備份逐 byte 比對相同）。

| 改壞的方式 | 預期 | 實際 |
|---|---|---|
| 共用表的 -54 公鑰大小 897 → 896 | T1 變紅 | 1 個失敗：T1「FN-DSA-512 (-54) has the sizes from its specification」。和共用表比對的那個測試仍通過，因為兩邊讀同一份檔案；這正是另外用規格書數值檢查的原因 |
| `SUPPORTED_ALGORITHMS` 拿掉 -55 | T1 變紅 | 4 個失敗：T1 的支援清單、大小表、-55 規格數值、選單選項 |
| `selectAlgorithm()` 改成選最後一個支援的 | T2 (c)(d) 變紅 | 5 個失敗：T2 (c)(d)、T5 (a)，以及既有的「selects first supported」與「signCount」兩個 |
| `credentialPublicKeyCose()` 的 kty 7 → 1 | T3 變紅 | T3 兩個失敗 |
| COSE_Key 的公鑰少放一個 byte | T3 變紅 | T3 兩個失敗 |
| `getAssertion()` 把簽章補零到 `SIGNATURE_BYTES` | T4 變紅 | T4 兩個失敗 |
| `selectAlgorithm()` 都不支援時改用 `defaultAlgorithm` | T5 (b) 變紅 | 2 個失敗：T5 (b) 與既有的「throws NotSupportedError」 |
| `selectAlgorithm()` 只要 `defaultAlgorithm` 有支援就優先選它 | T5 (a) 變紅 | 12 個失敗，包含 T5 (a)(b)（預設值 -48 也會蓋掉 RP 的選擇） |

### 獨立審查

交給沒看過實作過程的子代理，對照核准的 T1–T5 審查測試與 diff（11/24）。子代理實際跑了 `bun test src`（30 pass）、`bun run typecheck`，也另外打包到 scratchpad 確認可行；並依 RFC 8949 自行驗算 T3 的 10 個 bytes，結果正確。

**必須修正（已修正，`f2fd15e`）**
- `authenticator.test.ts` 的 `TestSigner.generateKeyPair()`、`sign()` 這次有改到，卻缺函式層級的註解（`CLAUDE.md`「語言與註解」）。已補上「做什麼、輸入與輸出」。

**建議與處理方式**

| 建議 | 處理 |
|---|---|
| 「依清單順序選第一個支援的」不是 WebAuthn §6.3.2 第 2 步（第 2 步只規定至少要有一個支援，否則回 `NotSupportedError`），而是 Level 2 第 7 步（產生新金鑰時，用清單中第一個支援的） | 已修正程式與測試註解（`f2fd15e`）。開工段落 T2 的依據欄是核准紀錄，保留原文，以這裡的說明為準。預期值不變，不算改弱測試 |
| T1「大小表比對共用表」對資料本身是同義反覆，抓不到共用表數值錯誤 | 已在測試註解寫明分工（`f2fd15e`）：這個測試只檢查接線，數值錯誤由規格書數值的測試抓。破壞檢查也證實了這一點 |
| `registryEntry()` 在模組載入時就丟錯，共用表少一筆時整個 background 起不來，連 ML-DSA 都不能用 | 不改。這是刻意的取捨：寧可整個 Extension 起不來，也不要選到沒有大小資訊的演算法；而且 T1 會先擋下來。理由已寫在函式註解 |
| 從資料夾外 import JSON，只拿 `extension/` 單獨建置會找不到檔案 | 記入待辦，Day 11 在 `extension/README.md` 註明建置需要整個 repo |
| `extension/README.md:13` 仍寫只支援 ML-DSA | 記入待辦，Day 11 文件同步處理（Day 7 之後 Extension 才真的能產生 Falcon 簽章，那時再改比較準確） |
| 開工段落 `liboqs-wasm-bridge.ts:171–202` 應為 `163–202` | 已修正 |
| `messages.ts` 可合成一行 `export type { SupportedAlg } from …` | 不改。實作時試過這個寫法：它不會把 `SupportedAlg` 帶進檔案本身，同檔案其他介面引用時會出現 `Cannot find name 'SupportedAlg'`，所以必須先 `import type` |
| T5 (a) 與 T3 沒有檢查 storage | 不改。核准的預期結果本來就沒有要求，屬於備註 |

**確認沒問題**：T1–T5 每個子情境都有測試，斷言和核准的一致，沒有被改弱；預期值都是字面值或規格書數值，沒有用 `encodeCbor()` 產生；開工段落列的破壞方式都會讓對應測試變紅；ML-DSA 的行為與大小不變；沒有動到禁止的資料夾，也沒有新增依賴套件；開工與完工段落的行號都對得上。
