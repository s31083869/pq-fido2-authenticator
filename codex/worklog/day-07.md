# Day 7：WASM bridge 支援 Falcon（F11、F12）

| 項目 | 內容 |
|---|---|
| 日期 | 2026-11-25（計畫原訂 11/22，已順延） |
| 分支 | `day-07`（從 `origin/main` 2da5682 開出） |
| 狀態 | 完工：T1–T6、破壞檢查與依獨立審查的修正都已完成；尚未 push，待使用者看過審查結果再開 PR |

---

## 開工

### 開工前補記

- Day 6 的 PR #8 三項 CI 都已通過，已於 11/24 合併。`day-06.md` 的狀態欄寫「尚未 push」，今天一併改為已合併。
- 基準：Python 103 個、Extension 30 個、前端 10 個測試全部通過（Day 6 完工時）。
- 本機工具鏈都在：`extension/emsdk`、CMake（`C:\Program Files\CMake`）、`C:\mingw64\bin\mingw32-make.exe`。
- 本機 WASM 用的 liboqs 原始碼 `extension/.deps/liboqs-emscripten-src` 目前在 `33815beb2ac404cba36ecf713f9fd5f1d868763a`（`0.15.0-60-g33815beb`），與決策 D4 一致；`liboqs.a` 是 5/22 用 `OQS_MINIMAL_BUILD=SIG_ml_dsa_44;SIG_ml_dsa_65;SIG_ml_dsa_87` 編出來的，**只有 ML-DSA**。
- `extension/public/wasm/pq_bridge.wasm`（94,891 bytes，5/30）**有進 git**，CI 與 Extension 都直接用這個檔案，所以重建後的 `.wasm` 要一起 commit。

### 今日目標

計畫書的 Day 7 有四項，對應 workflow.md F11、F12：

| 計畫項目 | 現況 | 今天要做的 |
|---|---|---|
| `pq_bridge.c` 加入 -54 → `Falcon-512`、-55 → `Falcon-1024` | `pq_alg_name()`（`pq_bridge.c:11–22`）只認得 -48/-49/-50，其他回 `NULL`，各函式再回 -1 | 加入兩個對應 |
| 編譯清單加入 `SIG_falcon_512;SIG_falcon_1024`，`LIBOQS_REF` 固定版本 | `setup-liboqs-emscripten.sh:10` 預設 `LIBOQS_REF=main`（會跟著上游變動），`:11` 只編 ML-DSA | `LIBOQS_REF` 改為完整 commit hash（D4），清單加入兩個 Falcon |
| 重建 `liboqs.a`、`pq_bridge.wasm` 與 extension | — | 跑兩個官方腳本（見「待你決定」第 1 點） |
| 確認 WASM 回報的金鑰與簽章大小正確；ML-DSA 既有測試仍通過 | **沒有任何測試會載入真的 WASM**：Extension 的 30 個測試都用假的簽章器 | 新增「載入真的 `pq_bridge.wasm`」的測試 T1–T4，以及跨實作驗章 T5 |
| （11/25 使用者追加，原排 Day 8）WASM 版 Falcon 跑官方 KAT | 11/13 只驗過**原生** liboqs 0.14.0；WASM 版從沒驗過 | T6：WASM 版 Falcon-512／1024 各 100 筆，和官方 `Falcon-Round3.zip` 的 KAT 逐 byte 一致 |

依序完成，每一項各自一個 commit（訊息格式 `Day 7: …`）：

1. 讓 bun 測試能載入真的 WASM，先用**目前的** `.wasm` 寫 T1–T4：ML-DSA 綠、FN-DSA 紅
2. 跨實作驗章 T5（WASM 簽章 → Python liboqs 驗章）
3. KAT：下載官方檔、產生雜湊表、寫 T6（重建前 FN-DSA 紅燈）
4. `pq_bridge.c` 對應、建置腳本、重建 `liboqs.a` 與 `pq_bridge.wasm`：T1–T6 全綠
5. 文件（三個 README、協議導覽）

**完成標準**（`FN-DSA-PLAN.md` Day 7，加上 Day 8 的 KAT）：`pq_bridge.wasm` 可產生 Falcon 金鑰與簽章，而且 WASM 版 Falcon 與官方 KAT 一致。

### 架構背景

#### 1. WASM 在 Extension 裡的位置

```
background（TypeScript）                      pq_bridge.wasm（C 編譯成 WebAssembly）
PQAuthenticator.makeCredential()
  └ LiboqsWasmSigner.generateKeyPair(-54)
      └ LiboqsWasmBridge.generateKeyPair(-54) ─→ pq_generate_keypair(-54, …)
                                                   └ pq_alg_name(-54) → "Falcon-512"   ← 今天加
                                                   └ OQS_SIG_new("Falcon-512")          ← liboqs.a 裡要有 Falcon（今天重編）
```

兩個地方都要改，缺一不可：
- `pq_alg_name()` 沒有 -54 → 回 `NULL` → 函式回 -1。
- `pq_alg_name()` 有 -54，但 `liboqs.a` 沒編進 Falcon → `OQS_SIG_new()` 回 `NULL` → 函式回 -2。

TypeScript 端的 `LiboqsWasmBridge` 收到負值就丟錯（`liboqs-wasm-bridge.ts:116–138`），所以 Day 6 之後 Extension 雖然「選得到」FN-DSA，產生金鑰時會失敗。

#### 2. 為什麼測試要載入真的 WASM

Day 6 的測試全部用假的簽章器，只證明「流程」對。今天改的是 C 程式與編譯清單，假的簽章器完全測不到。所以要讓 bun 測試直接讀 `extension/public/wasm/pq_bridge.wasm`，呼叫裡面真的 liboqs。

目前 `LiboqsWasmBridge` 只能用 `chrome.runtime.getURL()` 載入（`liboqs-wasm-bridge.ts:51`），bun 裡沒有 `chrome`。要拆出一個「從 bytes 載入」的函式，`loadFromExtensionResource()` 改成先 fetch 再呼叫它，Extension 的行為不變。

這也回答了計畫書的「ML-DSA 既有測試仍通過」：既有測試根本碰不到 WASM，必須另外寫。新測試先用**目前的** `.wasm` 跑一次，ML-DSA 應該綠燈（證明測試本身沒寫錯），FN-DSA 應該紅燈；重建後再跑，全部綠燈，而且 ML-DSA 的結果沒變。

#### 3. 怎麼分辨「不補滿」與「補滿」格式（T1、T3 的依據）

決策 D2 用不補滿格式（`Falcon-512`），不是補滿格式（`Falcon-padded-512`）。兩者的公鑰與私鑰大小相同，只有簽章不同：

| liboqs 名稱 | 公鑰 | 私鑰 | 簽章 | 依據 |
|---|---|---|---|---|
| `Falcon-512` | 897 | 1281 | 上限 752，長度不固定 | Falcon v1.2 第 3.11.6 節；liboqs `sig_falcon.h` |
| `Falcon-padded-512` | 897 | 1281 | 固定 666 | Falcon v1.2 第 3.11.3 節 |

所以 T1 檢查 WASM 回報的簽章大小是 752（不是 666），T3 檢查多次簽章的長度不全相同，兩個一起就能確認 C 端對應到的是不補滿格式。

另外，Falcon 簽章的第一個 byte 是標頭，依 Falcon v1.2 第 3.11.3 節為 `0x30 + logn`：FN-DSA-512（n = 512，logn = 9）為 `0x39`，FN-DSA-1024（logn = 10）為 `0x3A`。T3 也檢查這一點：它證明 WASM 簽出來的是 Falcon 的壓縮格式，而不只是長度剛好落在範圍內。

#### 4. 跨實作驗章（T5）

Extension 和 RP 用的是**兩份分別編譯**的 liboqs：

| | 版本 | 編譯方式 |
|---|---|---|
| Extension（簽章） | `33815beb`（0.15.0 之後，D4） | Emscripten → WebAssembly，只編 5 個演算法 |
| RP（驗章） | 0.14.0 | 原生 C，liboqs-python 呼叫 |

T5 讓 WASM 產生金鑰並簽章，再交給 RP 用的 Python liboqs 驗章（用 RP 自己的 `_cose_to_oqs()` 取演算法名稱，`rp_server/services.py:246`）。這是 `CLAUDE.md`「真實密碼學」要求的「產生金鑰 → 簽章 → RP 驗章」在 Extension 這一側第一次真的跑起來，也是簡報上說的「兩份獨立編譯的實作互相驗證」。

做法：寫一個 bun 腳本，用 WASM 對固定訊息簽章，把公鑰、訊息、簽章輸出成 JSON；pytest 呼叫這個腳本、讀 JSON、驗章。CI 的 Python 工作目前沒有 bun，要加一個 `setup-bun` 步驟（見「待你決定」第 3 點）。

#### 5. KAT 怎麼做（T6）

官方 KAT 檔（`Falcon-Round3.zip` 裡的 `falcon512-KAT.rsp`、`falcon1024-KAT.rsp`）是 Falcon 原作者用 NIST 的產生程式 `PQCgenKAT_sign.c` 跑出來的。每個檔案 100 筆，每筆有 `count`、`seed`、`mlen`、`msg`、`pk`、`sk`、`smlen`、`sm`。T6 要用 WASM 重現同樣的 100 筆，逐 byte 比對。

| 步驟 | 做法 | 依據 |
|---|---|---|
| 1. 決定性亂數 | 用 TypeScript 實作 NIST 的 AES-256 CTR DRBG（`rng.c` 的 `randombytes_init`／`randombytes`），AES 用 `node:crypto` | NIST `PQCgenKAT_sign.c`、`rng.c` |
| 2. 產生每筆的 seed 與 msg | DRBG 以 0, 1, …, 47 這 48 個 bytes 初始化；第 i 筆先取 48 bytes 當 seed，再取 33 × (i+1) bytes 當 msg | 同上；liboqs `tests/kat_sig.c:740–769` 也照這個流程 |
| 3. 產生金鑰與簽章 | 暫存 DRBG 狀態，用這筆的 seed 重新初始化，再呼叫 WASM 的 `generateKeyPair()`、`sign()`；WASM 要亂數時（`random_get`）改由 DRBG 供應；做完還原 DRBG 狀態 | `kat_sig.c:771–807` |
| 4. 轉成官方的 `sm` 格式 | liboqs 的簽章是「標頭 `0x39` ‖ nonce 40 bytes ‖ 壓縮簽章」；官方 `sm` 是「簽章長度（2 bytes 大端序，不含 nonce）‖ nonce ‖ msg ‖ `0x29`（1024 為 `0x2A`）‖ 壓縮簽章」 | `kat_sig.c:65–103`；Falcon 參考實作的 NIST API 格式 |
| 5. 比對 | 依官方格式組出整份 `.rsp` 文字，計算 SHA-256，和官方檔案的 SHA-256 比對；另外每筆各存一個雜湊，比對失敗時能指出第幾筆錯 | `CLAUDE.md`「避免球員兼裁判」第 2 條（預期值來自官方 KAT） |

為了讓 WASM 用 DRBG 而不是真的亂數，`LiboqsWasmBridge.fromBytes()` 要多一個「亂數來源」參數，預設仍是 `crypto.getRandomValues()`。**只有 KAT 測試會傳入 DRBG**；Extension 本身從不傳，註解會寫清楚。

不把 3 MB 的官方 `.rsp` 檔放進 git（計畫書 Day 10 的原則），只存它們的 SHA-256：
- `tests/kat/falcon-round3-kat.json`：官方 zip 與兩個 `.rsp` 檔的 SHA-256、下載網址、每筆的雜湊。
- `tests/kat/compute_falcon_kat_hashes.py`：從官方 `.rsp` 算出上面這份 JSON 的腳本，任何人下載官方檔後都能重算、核對。

步驟 1 的 DRBG 自己也是被測的程式，但它的輸出（每筆的 seed、msg）就在官方檔案裡，寫錯的話 T6 一定失敗，不會「一起錯」。

### 預計修改

| 檔案 | 預計修改 | 對應項目 |
|---|---|---|
| `extension/src/background/liboqs-wasm-bridge.ts:51–114` | 拆出 `LiboqsWasmBridge.fromBytes()`；`loadFromExtensionResource()` 改為 fetch 後呼叫它；補齊註解 | 1 |
| `extension/src/background/liboqs-wasm-bridge.test.ts`（新增） | T1–T4，讀 `public/wasm/pq_bridge.wasm` | 1 |
| `extension/scripts/wasm-sign-vectors.ts`（新增） | 用 WASM 對 5 個演算法各產生金鑰並簽一則固定訊息，輸出 JSON | 2 |
| `tests/integration/test_wasm_cross_verify.py`（新增） | T5 | 2 |
| `.github/workflows/ci.yml` | Python 工作加 `oven-sh/setup-bun`（版本與 Extension 工作相同） | 2 |
| `tests/kat/compute_falcon_kat_hashes.py`（新增） | 讀官方 `.rsp`，輸出雜湊表 JSON | 3 |
| `tests/kat/falcon-round3-kat.json`（新增） | 官方 zip 與 `.rsp` 的 SHA-256、下載網址、每筆的雜湊（由上面的腳本從官方檔案算出） | 3 |
| `tests/kat/nist-drbg.ts`（新增） | NIST AES-256 CTR DRBG | 3 |
| `tests/kat/wasm-falcon-kat.test.ts`（新增） | T6 | 3 |
| `extension/src/background/liboqs-wasm-bridge.ts` | `fromBytes()` 加「亂數來源」參數，預設 `crypto.getRandomValues()` | 3 |
| `.github/workflows/ci.yml`、`CLAUDE.md` | 必跑清單加入 `bun test tests/kat`（改 `CLAUDE.md` 需你同意，見「待你決定」第 5 點） | 3 |
| `extension/wasm/pq_bridge.c:11–22` | `pq_alg_name()` 加入 -54、-55；補齊這個函式的註解 | 4 |
| `extension/scripts/setup-liboqs-emscripten.sh:10–11` | `LIBOQS_REF` 預設改為 `33815beb2ac404cba36ecf713f9fd5f1d868763a`；`LIBOQS_MINIMAL_BUILD` 加入 `SIG_falcon_512;SIG_falcon_1024` | 4 |
| `extension/scripts/build-liboqs-wasm.sh:77–85` | （11/25 追加）`emcc` 加上 `-s STACK_SIZE=1048576`，修正 ML-DSA-65／87 與 FN-DSA-1024 的堆疊越界 | 4 |
| `extension/public/wasm/pq_bridge.wasm` | 重建（二進位檔） | 4 |
| `extension/scripts/README.md`、`extension/wasm/README.md`、`extension/public/wasm/README.md` | 編譯清單、對應表、測試會直接讀這個檔案 | 5 |
| `codex/PROTOCOL-GUIDE.html` | Day 7 進度、測試數；KAT 已在名詞表，補上「DRBG」 | 5 |
| `codex/worklog/day-06.md:7` | 狀態改為已合併 | 開工 |
| `codex/FN-DSA-PLAN.md` | 勾選 Day 7 | 完工 |

不會手動修改 `extension/.deps` 與 `extension/emsdk` 裡的任何檔案（見「待你決定」第 1 點）。

### 測試案例（已核准）

T1–T4 是 Extension 的 bun 測試，直接載入 `extension/public/wasm/pq_bridge.wasm`；T5 是跨元件的 pytest 整合測試。

| 編號 | 情境 | 預期結果 | 依據 | 實作前預期（用目前的 `.wasm`） |
|---|---|---|---|---|
| T1 | 對 5 個演算法呼叫 `publicKeyBytes()`、`secretKeyBytes()`、`signatureBytes()` | 等於共用表：-48 為 1312／2560／2420，-49 為 1952／4032／3309，-50 為 2592／4896／4627，-54 為 897／1281／752，-55 為 1793／2305／1462。-54 的簽章大小是 752 而不是 666（不是補滿格式） | 決策 D2、D3（C bridge 以測試檢查與共用表一致）；FIPS 204 Table 2；Falcon v1.2 第 3.11 節；workflow.md F12 | ML-DSA 綠；-54、-55 紅（C 端回 -1，bridge 丟錯） |
| T2 | 對 5 個演算法各呼叫 `generateKeyPair()` 兩次 | 公鑰、私鑰長度等於 T1 的值；兩次產生的公鑰不同（亂數來源有接上） | workflow.md F11、F12；FIPS 204、Falcon v1.2 的金鑰產生都使用隨機性 | ML-DSA 綠；FN-DSA 紅 |
| T3 | (a) ML-DSA 三個各簽同一則訊息一次 (b) FN-DSA-512、FN-DSA-1024 各用同一把私鑰對同一則訊息簽 20 次 | (a) 長度剛好等於 2420／3309／4627。(b) 每個簽章長度都不超過 752／1462；20 個長度不全相同；第一個 byte 為 `0x39`（512）／`0x3A`（1024） | FIPS 204（ML-DSA 簽章長度固定）；Falcon v1.2 第 3.11.3 節（標頭 `0x30 + logn`）、第 3.11.6 節（不補滿格式長度不固定）；workflow.md F10 | (a) 綠；(b) 紅 |
| T4 | 不支援的編號 -7（ES256）、-53、-56 | 三個大小函式都丟錯（C 端回 -1）；`generateKeyPair()` 也丟錯 | 決策 D1（只對應 -54/-55）；workflow.md F11 | 綠燈（回歸保護：確認只加了 -54/-55，沒有誤加鄰近編號） |
| T5 | 跨實作、真的 liboqs：WASM 對 5 個演算法各產生金鑰並簽一則固定訊息，交給 RP 的 `_cose_to_oqs()` 與 Python liboqs 0.14.0 驗章；另外把每個簽章的最後一個 byte 翻轉再驗一次 | 5 個原始簽章都驗證成功；5 個翻轉過的都驗證失敗 | `CLAUDE.md`「真實密碼學」；workflow.md F11、F15、F17；WebAuthn §7.2（RP 用公鑰驗章） | ML-DSA 綠；FN-DSA 紅（WASM 產生不了金鑰） |
| T6 | KAT：依架構背景第 5 點，用 DRBG 驅動 WASM 版 Falcon-512、Falcon-1024 各產生 100 筆，組成官方格式的 `.rsp` | (a) 100 筆的 `seed`、`msg` 與官方相同（證明 DRBG 正確）(b) 每筆的雜湊都和官方相同 (c) 整份 `.rsp` 的 SHA-256 等於官方 `falcon512-KAT.rsp`／`falcon1024-KAT.rsp` 的 SHA-256 | 官方 KAT（`Falcon-Round3.zip`，NIST PQC 第三輪提交包）；`CLAUDE.md`「KAT」與「避免球員兼裁判」第 2 條；計畫書 Day 8 | (a) 綠（DRBG 不依賴 WASM）；(b)(c) 紅（WASM 產生不了 Falcon 金鑰） |

重建後，T1–T6 全部要綠燈，而且 ML-DSA 的部分在重建前後都是綠燈：這就是「ML-DSA 行為不變」的證據。

ML-DSA 的 WASM 版 KAT 今天不做：NIST 第三輪的 Dilithium KAT 與正式的 ML-DSA（FIPS 204）不同，正式版的官方測試向量是 NIST ACVP 的 JSON 格式，需要另外寫比對程式。記入待辦，排在 Day 10。

**破壞檢查**（重建期間各做一次，再改回正確的版本重建）：
- `pq_alg_name()` 把 -54 對應到 `Falcon-padded-512`：T1（簽章大小 666 ≠ 752）與 T3 (b)（長度全部相同）必須變紅。
- `pq_alg_name()` 把 -54、-55 對調：T1 必須變紅。
- T5 的翻轉檢查本身就是破壞檢查：驗章函式若一律回傳成功，翻轉的那組會失敗。
- T6：把 DRBG 的計數器遞增改成從最低位以外的位置開始，(a) 必須變紅；用 `Falcon-padded-512` 重建一次（同上），(b)(c) 必須變紅。

### 待你決定（五點都已決定，見對齊紀錄）

1. **重建時會寫入 `extension/.deps`**（`CLAUDE.md`「不修改第三方或自動產生的資料夾」）：
   - 官方腳本 `setup-liboqs-emscripten.sh` 會刪掉並重建 `extension/.deps/liboqs-emscripten-build`（`:60–64`），也會在 `.deps/liboqs-emscripten-src` 執行 `git fetch` 與 `git checkout`（`:57–58`）。
   - (A，建議) 同意只透過這兩個官方腳本重建，`LIBOQS_REF` 指定為目前已經 checkout 的 `33815beb…`，所以原始碼不會變；Claude 不手動修改 `.deps` 裡的任何檔案。理由：這個資料夾本來就是腳本自動產生的，守則要防的是手改第三方程式碼。重建前先把現有的 `liboqs.a` 備份到 scratchpad，萬一失敗可以還原。
   - (B) 把建置目錄改到 `.deps` 以外（例如 scratchpad），再用 `LIBOQS_DIR` 指給 `build-liboqs-wasm.sh`。`.deps` 完全不動，但之後別人照 README 執行時，結果會在不同的位置。
2. **守則要求「liboqs 的任何變動（重建 WASM、改編譯清單）都必須通過 KAT」，但 KAT 測試排在 Day 8**：
   - (A，建議) Day 7 照計畫做 T1–T5，PR 說明明確寫「WASM 版 Falcon 的 KAT 由 Day 8 補上」。理由：Day 8 之前 Extension 只攔截 demo.yubico.com，它不宣告 FN-DSA，所以使用者碰不到 WASM 版 Falcon；T5 已經用另一份實作驗過簽章是對的。Day 8 做完 KAT 之後，這條守則才算真正滿足。
   - (B) 把 Day 8 的 WASM KAT 提前到今天。需要先取得官方 KAT 檔（11/13 驗證用的 `Falcon-Round3.zip`，本機目前找不到），今天的工作量約多 2 小時。
3. **T5 的跨實作驗章要在 CI 跑**：CI 的 Python 工作要加一個 `oven-sh/setup-bun` 步驟（`bun` 只用來執行腳本，不新增專案相依套件）。
   - (A，建議) 加。理由：不加的話，T5 在 CI 上只能跳過，等於沒有在乾淨的機器上驗證過。
   - (B) 不加。T5 在找不到 `bun` 時跳過，只在本機跑，結果記進工作紀錄。
4. **下載官方 KAT 檔**（T6 需要；本機找不到）：
   - 檔名 `Falcon-Round3.zip`，來源 NIST CSRC 第三輪提交包 `https://csrc.nist.gov/CSRC/media/Projects/post-quantum-cryptography/documents/round-3/submissions/Falcon-Round3.zip`，大小 4,067,127 bytes（以 HTTP HEAD 查得，伺服器標示最後修改 2024-09-29）。
   - 下載到 scratchpad 的一個新的空資料夾，只讀取裡面的 `falcon512-KAT.rsp`、`falcon1024-KAT.rsp`（純文字），不執行裡面的任何程式；zip 與 `.rsp` 都不進 git，只把 SHA-256 記進 `tests/kat/falcon-round3-kat.json`。
   - 同意嗎？
5. **KAT 測試放在哪、怎麼納入必跑清單**：
   - (A，建議) 依 `CLAUDE.md`「KAT 測試放 `tests/kat/`」，在專案根目錄用 `bun test tests/kat` 執行；`CLAUDE.md` 的必跑清單加一行 `bun test tests/kat`，CI 的 Extension 工作加一個同樣的步驟。`CLAUDE.md` 本身寫明「KAT 測試做好之後，納入上面的必跑清單」，但修改 `CLAUDE.md` 要你同意。
   - (B) 放在 `extension/src/` 底下，跟著 `bun test src` 一起跑，不用改必跑清單；但不符合「KAT 測試放 `tests/kat/`」。

### 待辦清單（中途發現、今天不處理）

- （實作中發現）Day 7 之前 Extension 路線實際上只能用 ML-DSA-44（堆疊越界，已修正）。Day 9 的 Extension 端到端清單要加上 ML-DSA-65（RP 預設第一個）的註冊與登入，確認在瀏覽器裡也正常。
- （獨立審查）Extension 的 bridge 是單例，WASM 一旦 trap（例如越界），同一個實例之後的呼叫都會壞；可考慮遇到 `RuntimeError` 時重建實例。Day 10 評估。
- （獨立審查）亂數來源的防呆：可改成名稱更明顯的選項，或加測試確認 `loadFromExtensionResource()` 每次產生的金鑰不同。Day 10 評估。
- （獨立審查）共用演算法表 `shared/pq-algorithms.json` 的 `description` 把 FN-DSA 的簽章上限 752／1462 也歸給 Falcon v1.2 第 3.11 節；實際來自參考實作 `falcon.h` 的 `FALCON_SIG_COMPRESSED_MAXSIZE`。Day 11 文件同步時修正。
- （獨立審查，待使用者決定）`CLAUDE.md` 必跑清單：`bun test tests/kat` 要在專案根目錄執行，與上面 `cd extension`、`cd frontend` 兩行的寫法容易混淆；「環境注意事項」寫 WASM 用 `extension/emsdk`，實際用的是 `C:\emsdk`（emcc 5.0.7，可重現目前的 `.wasm`）。兩處都要改 `CLAUDE.md`，需要使用者同意。→ 11/25 使用者同意兩處都修改，已完成：必跑清單那一行加註「在專案根目錄執行」，「環境注意事項」改為實際使用 `C:\emsdk` 的 emcc 5.0.7。
- ML-DSA 的 WASM 版 KAT（NIST ACVP 測試向量）排在 Day 10（見測試案例下方說明）。原生 liboqs（Python 端）的 KAT 納入專案也維持 Day 10。
- 沿用 Day 1–6 的待辦清單。

### 對齊紀錄

- 使用者提問（11/25）：`extension/.deps` 是做什麼的？什麼是 KAT？
- Claude 說明：
  - `.deps` 是建置腳本自動產生的本機建置資料夾，不進 git（`.gitignore:24`），內容為：`liboqs-emscripten-src`（liboqs 原始碼，294 MB，git clone 下來）、`liboqs-emscripten-build`（CMake 建置結果與 `liboqs.a`，2.6 MB，每次執行 setup 腳本都會刪掉重建）、`emscripten-cache`（Emscripten 的系統函式庫快取，45 MB）、`emscripten-shims`（腳本產生的 `emcc`／`emcmake` 轉接檔）。守則禁止修改，是為了不手改第三方程式碼；裡面的東西都可以由腳本重新產生。
  - 另外發現：`emscripten-shims/emcc` 指向 `C:\emsdk`，不是專案內的 `extension/emsdk`；本機有兩份 emsdk。重建前要確認用的是哪一份，並記進紀錄。
  - KAT（Known Answer Test）是演算法作者公布的標準答案：用固定的種子取代亂數，金鑰產生與簽章的結果必須和官方檔案逐 byte 相同。它能抓到 T5 抓不到的錯誤：兩邊都用 liboqs 的同一份原始碼，若原始碼或編譯有問題，簽章與驗章可能「一起錯」卻互相認可；KAT 的答案來自原作者的參考實作。Falcon 的金鑰產生與簽章用到浮點運算，WebAssembly 的編譯結果是否與原生一致，正是 KAT 要確認的。

- 待你決定（11/25）：使用者回答「都採 A，並且今天把 KAT 測試也納入今天要完成的目標」。第 1 點 (A)：只透過官方腳本重建 `.deps`；第 3 點 (A)：CI 的 Python 工作加 bun。第 2 點原本建議 KAT 留到 Day 8，依使用者指示改為**今天就做**（等同原本的 B），新增 T6 與第 4、5 點。

- 第 4 點（11/25）：使用者同意下載。下載結果：
  - `Falcon-Round3.zip`：4,067,127 bytes（與 HEAD 查得的大小相同），SHA-256 `fd58f0454f6bfb4713734e60b2d2d75d96fbae62d5180fceeef1039df5362f44`，共 165 個項目。
  - 只取出兩個 `.rsp`（zip 內路徑 `Falcon/falcon-round3/KAT/`），其他檔案沒有解壓、沒有執行：
    - `falcon512-KAT.rsp`：1,250,115 bytes，SHA-256 `dd75c946fdedef4ec46a2bee7e10c65c9126f1a839b9ced6921fd45f7354b5cd`
    - `falcon1024-KAT.rsp`：1,757,286 bytes，SHA-256 `036a0bf5260573cec44977284dfef756cd1143db9961b981bd1fb55828acb20d`
  - 格式：第一行 `# Falcon-512`（或 `# Falcon-1024`）再接一個空行；每筆 8 行（`count`、`seed`、`mlen`、`msg`、`pk`、`sk`、`smlen`、`sm`，16 進位大寫），每筆後面都接一個空行（包含最後一筆）；只有 LF 換行、沒有 CR。
  - 注意：liboqs 自己的 `tests/KATs/sig/kats.json` 記錄的 Falcon-512 雜湊（`f4f23c11…`）和官方檔案的 SHA-256 不同。liboqs 算的是它自己 `kat_sig` 程式的輸出，格式和官方檔案不完全相同，例如最後一筆後面不加空行（`kat_sig.c:797–800`）。T6 比對的是**官方檔案**，不是 liboqs 的雜湊。

- 使用者說明今天的內容（11/25）：「今天要讓 WASM 加入 Falcon；這會用到 liboqs，也會影響 `extension/.deps`。當初學長不希望改到 liboqs 的原始程式碼，所以禁止動這個資料夾；現在是為了加入 Falcon，用指令重建。加入 Falcon 之後要驗證簽章是否正確，所以找了 NIST 的 KAT 檔來驗證。」方向正確。Claude 補充一個細節：重建用的是**專案自己的**建置腳本（`extension/scripts/`），它呼叫 CMake 與 Emscripten 把 liboqs 原始碼重新編譯；liboqs 原始碼本身不改，改的只有「要編哪些演算法」的清單。以確認問題檢查 T5 與 T6 的分工、重建前先跑測試的用意、752 與 666 的差別。

- 確認問題（11/25）：
  - 問題 1（T5 與 T6 差在哪、為什麼兩個都要）：使用者回答「一個是看 liboqs 是否有正確使用，另一個是確認實作結果是否跟官方 KAT 相同」。大致對上。Claude 補充：T5 證明 WASM 的輸出能被**另一份編譯**的 liboqs 接受（C 對應、資料傳遞、WASM 與 RP 能互通）；但兩邊都來自 liboqs 的同一份原始碼，原始碼或編譯若有問題，可能一起錯。T6 的答案來自 Falcon **原作者**的參考實作，與 liboqs 無關，才抓得到這類錯誤（例如 WASM 的浮點運算結果與原生不同）。
  - 問題 2（重建前先跑一次，ML-DSA 與 FN-DSA 會是什麼燈、為什麼要先跑）：使用者回答「綠燈、紅燈，原因不太清楚」。燈號正確，原因有落差。Claude 補充：ML-DSA 綠燈證明測試本身寫對了（不是因為測試寫錯才紅）；FN-DSA 紅燈證明測試真的偵測得到「沒有 Falcon」（不是永遠綠）；重建後 ML-DSA 仍綠，才能說 ML-DSA 的行為沒變。這也是 `CLAUDE.md` 要求「實作前跑出紅燈並記錄」的理由。
  - 問題 3（T1 檢查 752 而不是 666 是在防什麼）：使用者回答「防簽章大小的上限太小」。有落差。Claude 補充：666 是**補滿格式**（`Falcon-padded-512`）的固定簽章長度。如果 C 端把 -54 誤對應到補滿格式，公鑰、私鑰大小完全相同，簽章也能被 `Falcon-512` 驗過（補滿與不補滿可以互相驗證，計畫書第 2 節），所以 T2、T5 都會通過，只有「簽章大小 752」與 T3 的「長度不固定」、T6 的 KAT 抓得到。它防的是「選錯 Falcon 的格式」，違反決策 D2。

- 第 5 點（11/25）：使用者同意採 (A)，KAT 測試放 `tests/kat/`，`CLAUDE.md` 的必跑清單與 CI 加入 `bun test tests/kat`（使用者同意修改 `CLAUDE.md`）。

- 使用者重述（11/25）：問題 2「如果沒先跑那一次，重建後全部變綠，無法分辨是真的修好了，還是測試根本什麼都沒測到」；問題 3「666 不是上限，而是補滿格式（`Falcon-padded-512`）的固定簽章長度，T1 要防的是選錯 Falcon 的格式」。兩句都引用 Claude 的說明原文；重點正確，視為已對上。

- 使用者核准測試案例 T1–T6（11/25）。

### 實作中的發現：現有的 `pq_bridge.wasm` 無法使用 ML-DSA-65／87（11/25）

寫好 T1–T4、用**目前的** `.wasm` 跑紅燈時，預期 ML-DSA 全綠，實際上 ML-DSA-65、ML-DSA-87 的 T2、T3a 失敗：`RuntimeError: Out of bounds memory access`（發生在 `pq_generate_keypair`），之後同一個 WASM 實例的呼叫也跟著出現 `Out of bounds call_indirect`。

診斷（只輸出到 scratchpad，Emscripten 快取也放 scratchpad，沒有寫入 `extension/public/wasm` 與 `.deps`）：

| 測試用的 WASM | ML-DSA-44 | ML-DSA-65 | ML-DSA-87 |
|---|---|---|---|
| git 裡的 `pq_bridge.wasm`（每個演算法各用全新的實例） | 正常 | 越界 | 越界 |
| 用 `C:\emsdk` 的 emcc 5.0.7、和 `build-liboqs-wasm.sh` 相同的參數重編 | 正常 | 越界 | 越界 |
| 同上，只多加 `-s STACK_SIZE=1048576`（1 MB） | 正常 | 正常 | 正常 |

- 第二列重編出來的檔案和 git 裡的 `pq_bridge.wasm` **逐 byte 相同**：證明現有的 WASM 就是用 `C:\emsdk` 這套工具鏈、照目前的腳本編出來的，建置可以重現。
- 原因：Emscripten 預設的堆疊只有 64 KB（放在 WASM 的線性記憶體裡），ML-DSA-65／87 產生金鑰時的暫存陣列超過這個大小，寫到堆疊範圍之外，破壞了其他資料。ML-DSA-44 用得少，所以正常。這與瀏覽器無關，Chrome 裡也一樣。
- 影響：Day 7 之前，Extension 實際上只能用 ML-DSA-44；RP 預設把 ML-DSA-65（-49）排第一，Extension 會選 -49，然後在產生金鑰時失敗。這是 Day 7 之前就存在的問題，由今天新增的「真的 WASM 測試」第一次抓到。
- 測試案例的預期結果沒有改，改的是「實作前預期」那一欄的判斷：ML-DSA-65／87 的 T2、T3a 在重建前是紅燈。
- 與今天的目標直接相關：FN-DSA-1024 的簽章函式在堆疊上放了 72 KB 的暫存區（`.deps/liboqs-emscripten-src/src/sig/falcon/pqclean_falcon-1024_clean/pqclean.c:126` 的 `uint8_t b[72 * 1024]`），也超過 64 KB。不加大堆疊，今天加入的 FN-DSA-1024 一樣會越界。
- 使用者決定（11/25）：**今天加大堆疊**。`build-liboqs-wasm.sh` 加上 `-s STACK_SIZE=1048576`（1 MB），與 Falcon 一起重建；T2、T3a 的 ML-DSA-65／87 由紅轉綠，就是這個修正的證據。

---

## 完工

### 實際修改

| 檔案:行號範圍 | 改了什麼 | 目的 | commit |
|---|---|---|---|
| `extension/wasm/pq_bridge.c:11–36` | `pq_alg_name()` 加入 -54 → `Falcon-512`、-55 → `Falcon-1024`；補齊函式註解 | F11；決策 D1、D2 | `b5cfbb4` |
| `extension/scripts/setup-liboqs-emscripten.sh:10–15` | `LIBOQS_REF` 預設由 `main` 改為 `33815beb2ac404cba36ecf713f9fd5f1d868763a`；`LIBOQS_MINIMAL_BUILD` 加入 `SIG_falcon_512;SIG_falcon_1024` | F12；決策 D4 | `b5cfbb4` |
| `extension/scripts/build-liboqs-wasm.sh:77–89` | `emcc` 加上 `-s STACK_SIZE=1048576`（註解在 77–79，旗標在 86） | 修正 ML-DSA-65／87 與 FN-DSA-1024 的堆疊越界（使用者 11/25 同意） | `b5cfbb4` |
| `extension/public/wasm/pq_bridge.wasm` | 重建：94,891 → 251,132 bytes，SHA-256 `4dea651c…68a2`；工具鏈 `C:\emsdk` emcc 5.0.7 | F11、F12 | `b5cfbb4` |
| `extension/src/background/liboqs-wasm-bridge.ts:49–167` | 新增 `RandomBytesSource`、`systemRandomBytes`、`fromBytes(wasmBytes, randomBytes)`；`loadFromExtensionResource()` 改為 fetch 後呼叫 `fromBytes()`；改用 `compile` + `instantiate(module)` | bun 測試能載入真的 WASM；KAT 能注入 DRBG；Extension 行為不變 | `b5cfbb4` |
| `extension/src/background/liboqs-wasm-bridge.ts:67–220` | 類別註解；`fromBytes()` 補 `CompileError`／`LinkError`；三個大小函式的錯誤訊息帶出 C 端代碼（`code=-1`／`-2`）並補齊註解 | 依獨立審查；T4 能區分 -1 與 -2 | `2641264` |
| `extension/src/background/liboqs-wasm-bridge.test.ts:1–93`（新增） | T1–T4；依審查加嚴 T2（第二把私鑰長度）、T4（`code=-1`），T1 註明 752／1462 的參考實作來源 | T1–T4 | `b5cfbb4`、`2641264` |
| `extension/scripts/wasm-sign-vectors.ts:1–58`（新增） | 用 WASM 對 5 個演算法產生金鑰並簽固定訊息，輸出 JSON | T5 | `918ef7f` |
| `tests/integration/test_wasm_cross_verify.py:1–87`（新增） | T5 | T5；`CLAUDE.md`「真實密碼學」 | `918ef7f` |
| `tests/kat/compute_falcon_kat_hashes.py:1–134`（新增） | 從官方 zip 算出雜湊表；確認拆出的 100 筆能逐 byte 組回原檔 | T6 的預期值來源 | `4b7d5a8` |
| `tests/kat/falcon-round3-kat.json`（新增，47 KB） | 官方 zip 與兩個 `.rsp` 的 SHA-256、每筆的 `seedMsgSha256` 與 `entrySha256` | T6 | `4b7d5a8` |
| `tests/kat/nist-drbg.ts:1–104`（新增） | NIST AES-256 CTR DRBG（審查後補類別註解） | T6 | `4b7d5a8`、`2641264` |
| `tests/kat/wasm-falcon-kat.test.ts:1–140`（新增） | T6 | T6；計畫書 Day 8 的 KAT | `4b7d5a8` |
| `.github/workflows/ci.yml:45–50、88–93` | Python 工作加 `oven-sh/setup-bun`；Extension 工作加「KAT（WASM 版 Falcon）」步驟（從根目錄執行 `bun test tests/kat`） | 「待你決定」第 3、5 點 | `4b7d5a8` |
| `CLAUDE.md:87` | 必跑清單加一行 `bun test tests/kat` | 「待你決定」第 5 點（使用者同意修改 `CLAUDE.md`） | `4b7d5a8` |
| `pyproject.toml:31–35` | `testpaths` 加入 `tests/kat`；審查後補註解 | `CLAUDE.md`「新增 `tests/` 資料夾後要同步」 | `4b7d5a8`、`2641264` |
| `extension/tsconfig.json:17` | `include` 加入 `scripts/wasm-sign-vectors.ts` 與 `../tests/kat` | 讓新的 TypeScript 也經過型別檢查 | `4b7d5a8` |
| `codex/PROTOCOL-GUIDE.html` | 更正第 10 章「Extension 路線 ML-DSA-65／87 也能用」；Day 7 進度與測試數（審查後更正 Python 103 → 108）；第 11 章新增 DRBG、堆疊、WASI | 文件 | `b52e9d8`、`2641264` |
| `extension/scripts/README.md`、`extension/wasm/README.md`、`extension/public/wasm/README.md` | 編譯清單、固定版本、堆疊、對應表、直接讀 WASM 的測試 | 文件 | `b52e9d8` |
| 本檔開工段落、`codex/worklog/day-06.md:7` | 開工文件；Day 6 狀態改為已合併 | 文件 | `40bea82` |

和開工文件的差異：
- 第 1–3 項的測試都在重建**之前**寫好並跑過紅燈，但守則規定「失敗的測試不 commit」，所以實際 commit 的順序改成：重建與 T1–T4 一起（`b5cfbb4`），再 T5（`918ef7f`），再 KAT（`4b7d5a8`），每個 commit 都是全綠。
- CI 的兩個修改都放在 KAT 那個 commit（同一個檔案，不能拆成兩個 commit）。所以單看 `918ef7f`，CI 的 Python 工作會因為沒有 bun 而失敗；PR 的 CI 只跑最新的 commit，不影響合併。
- `build-liboqs-wasm.sh` 的 `STACK_SIZE` 是實作中追加的（見「實作中的發現」）。
- 開工段落引用的 `setup-liboqs-emscripten.sh:57–58`（`git fetch`／`git checkout`）、`:60–64`（刪除建置目錄）是修改前的行號，現在是 `:61–62`、`:64–68`；預計修改表寫的 `build-liboqs-wasm.sh:77–85` 實際為 `:77–89`。

### 測試結果（實作前 → 實作後）

| 階段 | 結果 |
|---|---|
| 基準（開工時） | Python 103、Extension 30、前端 10，全部通過 |
| T1–T4 實作前（目前的 `.wasm`） | 7 pass、11 fail。FN-DSA 的 T1、T2、T3b 失敗：`invalid public key size for alg=-54／-55`（C 端回 -1）。**另外 ML-DSA-65／87 的 T2 與三個 T3a 失敗**：`Out of bounds memory access`／`Out of bounds call_indirect`（見「實作中的發現」）。T4 通過 |
| T5 實作前（目前的 `.wasm`，重建前執行） | 1 pass（ML-DSA-44）、4 fail：-49、-50 越界（`Out of bounds memory access`），-54、-55 產生不了金鑰（`invalid public key size`） |
| T6 實作前（目前的 `.wasm`，重建前執行） | 2 fail，都在 (b) 的第 0 筆（`Expected: -1, Received: 0`）；(a) 已通過，證明 DRBG 產生的 100 筆 seed／msg 都和官方相同 |
| 重建後 | Extension 48 個（原 30 + T1–T4 共 18）全部通過；T5 5 個全部通過；T6 2 個全部通過（約 7 秒） |
| 最終（每次 commit 前） | Python 108、Extension 48、前端 10、KAT 2，全部通過；ruff、Extension typecheck、前端 lint 與 tsc 都通過 |

額外的交叉印證：官方檔案第 0 筆的雜湊（Falcon-512 `da27fe8a…`、Falcon-1024 `e699d88e…`）等於 liboqs `tests/KATs/sig/kats.json` 的 `single` 值，證明我們拆「一筆」的方式和 liboqs 相同。

### 破壞檢查

壞掉的版本都從 scratchpad 的 C 檔副本編譯，不改 repo 裡的 `pq_bridge.c`；每次做完都把正確的 `pq_bridge.wasm` 複製回來，並逐 byte 比對確認還原。

| 改壞的方式 | 預期 | 實際 |
|---|---|---|
| `pq_alg_name()` 把 -54、-55 對調 | T1 變紅 | T1、T2、T3b 的 FN-DSA 共 6 個失敗；T6 兩個都失敗 |
| `pq_alg_name()` 把 -54 對應到 `Falcon-padded-512`（另外在 scratchpad 編一份含 `SIG_falcon_padded_512` 的 `liboqs.a`，`.deps` 裡的不動，事後核對雜湊相同） | T1（666 ≠ 752）、T3b 變紅 | T1 與 T3b 的 FN-DSA-512 失敗；T6 Falcon-512 失敗。**T2 與 T5 全部通過**：補滿格式的金鑰大小相同，簽章也能被 `Falcon-512` 驗過，所以只有大小、長度、KAT 抓得到，與對齊時問題 3 的說明一致 |
| DRBG 的計數器改成從第 14 個 byte 開始遞增 | T6 (a) 變紅 | T6 兩個都失敗，失敗位置在 `wasm-falcon-kat.test.ts:128`，也就是 (a) |
| T5 的翻轉檢查 | 驗章若一律成功就會失敗 | 寫在測試裡，每次執行都會檢查 |

### 獨立審查

交給沒看過實作過程的子代理，對照核准的 T1–T6 審查測試與 diff（11/25）。子代理實際跑了 `bun test tests/kat`（2 pass）、Extension `bun test src`（48 pass）與 typecheck、T5（5 pass）、ruff、`pytest --collect-only`（108 個）；沒有執行任何建置，也沒有動 `.deps`。

**結論：程式與測試本身沒有必須修正的錯誤。** 子代理另外做了幾項獨立驗證：
- 用 WASM 加 DRBG 產生 liboqs 自己的 KAT 格式，SHA-256 分別是 `f4f23c11…`、`46f9682e…`，與 liboqs `kats.json` 的 `all` 完全相同（第三個獨立來源）。
- 讀 WASM 的全域變數：舊檔 `__stack_pointer` 初值 71,232，新檔 1,113,584，差值正好對應 64 KB 與 1 MB，證明新檔真的用 1 MB 堆疊編譯。
- 各簽 2,000 次統計：Falcon-512 長度 647–663（17 種）、Falcon-1024 長度 1260–1284，T3b「20 次長度全同」的機率約 1e-15 以下，不會偶發失敗。
- 把亂數來源換成「不動」或「全填 0」，T2 會失敗，證明「兩次金鑰不同」這個檢查有效。

**必須修正（已處理）**

| 項目 | 處理 |
|---|---|
| 協議導覽第 10 章的 Python 測試數仍是 103（實際 108） | 已更正（`2641264`） |
| 工作紀錄缺紅燈與破壞檢查的實際結果 | 審查時完工段落尚未寫入工作紀錄；現在已補上本段的「測試結果」與「破壞檢查」，並註明 T5、T6 的紅燈是在重建前用舊的 `.wasm` 跑的 |

**建議與處理方式**

| 建議 | 處理 |
|---|---|
| T2 少檢查第二把私鑰的長度 | 已加（`2641264`），屬於加嚴 |
| T4 沒有區分 C 端回 -1 或 -2 | 大小函式的錯誤訊息改為帶出代碼，T4 確認是 `code=-1`（`2641264`），屬於加嚴 |
| 752／1462 的依據：規格書第 3.11 節列的是補滿格式的大小，不補滿格式的上限來自參考實作 `falcon.h` 的 `FALCON_SIG_COMPRESSED_MAXSIZE` | 測試註解已補上參考實作來源（`2641264`）；共用表 `description` 也引用第 3.11 節，記入待辦，Day 11 文件同步時修正 |
| 工作紀錄行號（`setup-liboqs-emscripten.sh` 修改後位移、`build-liboqs-wasm.sh` 範圍） | 完工段落已用新行號，並在「和開工文件的差異」說明 |
| `CLAUDE.md` 必跑清單的 `bun test tests/kat` 排在 `cd frontend && …` 之後，照順序在同一個 shell 執行會在 frontend 目錄下跑 | 使用者同意後修改：那一行加註「在專案根目錄執行」 |
| `LiboqsWasmBridge`、`NistCtrDrbg` 缺類別註解；`fromBytes()` 的 `@throws` 不完整；`pyproject.toml` 註解沒提 `tests/kat` | 都已補（`2641264`） |
| 亂數來源可改成名稱更明顯的選項，或加測試確認 `loadFromExtensionResource()` 不用決定性亂數 | 不改。子代理確認實際流程只有 `liboqs-wasm-signer.ts:10` 呼叫 `loadFromExtensionResource()`，它不轉傳亂數參數；`fromBytes()` 的註解已明寫只有 KAT 測試能傳。記入待辦，Day 10 測試補強時再評估 |
| Extension 的 bridge 是單例，WASM 一旦 trap，同一個實例之後都會壞 | 記入待辦（不屬於今天的範圍） |
| 實際工具鏈是 `C:\emsdk` 的 emcc 5.0.7，`CLAUDE.md`「環境注意事項」寫的是 `extension/emsdk` | 使用者同意後修改「環境注意事項」為實際路徑 |
| 完工段落要說明 commit 安排、`918ef7f` 單獨看 CI 會紅 | 已寫在「和開工文件的差異」 |
| 名詞表加 WASI | 已加（`2641264`） |

**確認沒問題**：T1–T6 每個子情境都有測試，沒有被改弱或跳過；KAT 雜湊確實由腳本從官方檔案算出，並有三個獨立來源互相印證（NIST 公開的第 0 筆、liboqs 的 `single`、liboqs 的 `all`）；DRBG 逐行對照 NIST `rng.c` 一致；`sm` 轉換與 `kat_sig.c:65–103` 一致；CI 的 KAT 步驟會在根目錄執行；`.deps/liboqs-emscripten-src` 停在 33815beb 且 `git status` 乾淨，`oqsconfig.h` 裡補滿格式未啟用；`CLAUDE.md` 的修改只有使用者同意的那一行；commit 訊息格式正確。
