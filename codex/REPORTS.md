# PQ-FIDO2 專案評估報告（v7）

## 0. 文件同步狀態

1. 目前單一來源為 `codex/REPORTS.md`。
2. 根目錄 `REPORTS.md` 已不存在，避免雙檔漂移。
3. 後續 commit/PR 皆以本檔作為決策與規格追蹤文件。

## 1. 本版前提（已同步）

1. 前端介面與 RP Server：`https://demo.yubico.com/webauthn-developers`
2. 開發範圍：只做瀏覽器/驗證器（Chrome Extension）
3. 模式：`Post-Quantum WebAuthn API`（攔截/改寫，由使用者情境決定是否啟用）
4. 演算法：只支援 `ML-DSA-44/65/87`（COSE `-48/-49/-50`）
5. 目前階段：同時研究與考慮應用性，規格仍在確認中
6. 暫不處理 fallback

---

## 2. 可行性結論

在你限定的邊界下可行。你先前的 Python + Playwright + 自定義 authenticator 已在 Yubico demo 成功完成註冊，代表核心流程可打通。

目前本專案重點是把該能力搬到一般使用者可用的 Chrome extension 形態。

---

## 3. 三個關鍵點白話說明（你提到不清楚的部分）

1. `credentialPublicKey` COSE 結構定義
- 這是註冊時放在 `attestationObject.authData` 裡的「公鑰描述格式」。
- 你要先定義：
  - key type（kty，注意這和 WebAuthn descriptor 的 `type: "public-key"` 是不同層級）
  - alg（此案是 `-48/-49/-50`）
  - 真正的 PQ 公鑰 bytes 放在哪個 COSE 欄位
- 目的：讓 RP 在解析 attestation 時，知道如何取出公鑰並驗證 assertion 簽章。

2. `authenticatorData` flags/signCount 規則
- `authenticatorData` 是 assertion/attestation 都會帶的核心欄位。
- 你要固定兩件事：
  - flags 怎麼設（UP/UV/AT）
  - `signCount` 如何遞增與何時初始化
- 目的：讓 RP 端在驗證時有一致語義，避免被判定資料格式或狀態異常。

3. `attestation fmt` 先用 `none`
- `fmt: "none"` 表示不提供可驗證的 attestation statement 憑證鏈。
- 好處：流程最簡化，先聚焦 credential 生成與 assertion 驗證。
- 你已決議先用 `none`，這是合理的 PoC 起點。

---

## 4. 與 Yubico payload 對齊的最小規格

參考 `repomix-output-Yubico-python-fido2.md`，攔截層至少保持以下欄位語義。

註冊（create）request options：
- `publicKey.rp`
- `publicKey.user.id/name/displayName`
- `publicKey.challenge`
- `publicKey.pubKeyCredParams`
- `publicKey.timeout`（optional）
- `publicKey.excludeCredentials`（optional）
- `publicKey.authenticatorSelection`（optional）
- `publicKey.attestation`（optional）
- `publicKey.extensions`（optional）

註冊（create）response payload：
- `type`
- `id`
- `rawId`
- `response.clientDataJSON`
- `response.attestationObject`
- `response.transports`（optional）
- `clientExtensionResults`

登入（get）request options：
- `publicKey.challenge`
- `publicKey.timeout`（optional）
- `publicKey.rpId`（optional）
- `publicKey.allowCredentials`（optional）
- `publicKey.userVerification`（optional）
- `publicKey.extensions`（optional）

登入（get）response payload：
- `type`
- `id`
- `rawId`
- `response.clientDataJSON`
- `response.authenticatorData`
- `response.signature`
- `response.userHandle`
- `clientExtensionResults`

---

## 5. 已確認決策（2026-02-07）

1. UV：你要求「強 UV」
- 現況標記：需求已確認，但技術方案尚未定稿（見第 6 節）。

2. attestation 策略
- 先固定 `attestation = none`。

3. 演算法策略
- 預設 `ML-DSA-44 (-48)`。
- 同時支援 `-49/-50`。
- 驗證器依 RP 傳入的 `pubKeyCredParams` 選擇/生成。

4. 攔截啟用範圍
- v1 僅在 `demo.yubico.com` 啟用。
- 未來再開放任意網域手動開關。

5. PQ-only 嚴格模式
- 若 `pubKeyCredParams` 不含 `-48/-49/-50`，直接拋錯。

6. `credentialPublicKey`/`type` 對齊策略
- WebAuthn credential descriptor 維持 `type: "public-key"`。
- COSE `credentialPublicKey` 另行定義 `kty/alg/公鑰欄位`，貼近既有 WebAuthn 結構但承載 PQ 公鑰。

7. `authenticatorData` 預設規則
- 註冊（create）：`flags = UP + UV + AT`（預設成功 UV 才回應），`signCount = 0`。
- 驗證（get）：`flags = UP + UV`，每次成功 assertion 後 `signCount += 1`（首筆 assertion 為 1）。

8. `allowCredentials` / `excludeCredentials` 的定位
- `excludeCredentials`：註冊時避免重複建立已存在 credential。
- `allowCredentials`：驗證時限制只允許指定 credential 通過。
- 兩者視為同一套 credential 存取控制在 create/get 兩端的對應機制。

9. `liboqs` 採用策略（v1）
- 建議優先採用「Extension 內 WASM」路線，降低終端安裝門檻。
- v1 目標是不要求使用者另行安裝本機 `liboqs`。
- 若後續因強 UV 需要 Native Host，再評估 Host 端改用本機 `liboqs`。

---

## 6. 主要開放風險：強 UV 可行性

你問「強 UV 能不能做、是否需要額外 process」。

目前可行路徑如下：
1. Extension 純前端方案：可做「軟體 UV」（PIN/密碼/確認），但通常不等於 OS 級強 UV。
2. 要求 OS 級強 UV（如 Touch ID / Windows Hello）：通常需要原生橋接（Native Messaging Host 或其他外部元件）。
3. 一旦需要外部元件，終端使用門檻會上升，會影響應用性。

你問「能不能自動建立 process，驗證完 UV 就釋放資源」：
1. 可行，但通常要用 `Native Messaging Host`。
2. Extension 在需要 UV 時呼叫 `chrome.runtime.connectNative()`，由瀏覽器啟動 host process。
3. UV 完成後關閉連線（port close），host 可自動結束並釋放資源。
4. 限制是：使用者仍需先安裝/註冊 native host（一次性），無法做到完全零安裝。

因此本案現況是：
- 強 UV 是已確認需求。
- 但「不增加安裝/操作負擔」與「OS 級強 UV」兩者存在張力，需你在規格上取捨。

---

## 7. 建議架構（Chrome Extension v1）

1. `content script` 於 `document_start` 注入 `main-world hook`。
2. 攔截 `navigator.credentials.create/get`，做 ArrayBuffer/base64url 正規化。
3. 將請求送至 extension runtime 的 PQ authenticator。
4. PQ authenticator 執行：
- challenge 綁定
- 依 `pubKeyCredParams` 選擇 `-48/-49/-50`
- 生成 keypair
- 生成 `authenticatorData` 與 `attestationObject(fmt=none)`
- assertion 簽章與 `signCount` 更新
5. 回傳符合 `PublicKeyCredential` 外形的 payload。
6. 限定網域啟用（`demo.yubico.com`）。

---

## 8. 近期里程碑（規格確認中）

### M1: 註冊規格凍結
- 凍結 `credentialPublicKey` COSE mapping（含 `-48/-49/-50`）
- 凍結 `authenticatorData` flags 與初始 `signCount`
- 凍結 `attestationObject`（`fmt=none`）

### M2: Assertion 規格凍結
- 凍結簽章輸入格式
- 凍結 `signCount` 遞增規則
- 凍結 `allowCredentials` 選擇與錯誤行為

### M3: Extension PoC
- 在 Yubico demo 完成註冊與登入成功路徑
- 產出可重現測試步驟與封包樣本

---

## 9. 下一步建議

先做 M1/M2 規格凍結文件，再開始正式實作 extension。你現在的方向已足夠明確，剩下最大不確定只在「強 UV 方案」是否接受外部元件。

另外可並行補一組安裝檢查腳本：
- `check-prereqs`：檢查 Native Host 註冊狀態與 WASM 載入可用性。
- `install-clean`：僅在選擇 Native Host 路線時，協助一次性安裝與 smoke test。

---

## 10. Decision Log（for commit/PR）

1. 2026-02-07：目標站點固定為 `https://demo.yubico.com/webauthn-developers`，先以該 RP 驗證流程為基準。
2. 2026-02-07：專案範圍固定為 Chrome extension（瀏覽器/驗證器），不改動 RP 後端。
3. 2026-02-07：流程採 PQ-only，不考慮 fallback 到傳統演算法。
4. 2026-02-07：演算法固定支援 `ML-DSA-44/65/87`（`-48/-49/-50`），預設 `-48`。
5. 2026-02-07：`attestation` 先固定為 `none`，先打通 create/get 主流程。
6. 2026-02-07：`authenticatorData` 預設為 create `UP+UV+AT`、get `UP+UV`，`signCount` 註冊為 0，成功驗證後遞增。
7. 2026-02-07：`excludeCredentials` 與 `allowCredentials` 定位確認為 create/get 兩端的 credential 存取控制。
8. 2026-02-07：v1 優先走 Extension 內 WASM，避免要求終端安裝本機 `liboqs`。
9. 2026-02-07：強 UV 仍為需求，但目前列為開放風險；若採 OS 級 UV，可能需 Native Messaging Host（一次性安裝）。
10. 2026-02-07：開發順序先完成 M1/M2 規格凍結，再進入 extension 實作與 trial-and-error。
11. 2026-02-08：觀測到 Yubico create options 會帶 `attestation: "direct"`；v0.1 仍固定回傳 `fmt=none`，先以可運作流程為優先。
12. 2026-02-08：Legacy Playwright 樣本確認 create flags=`0x45`、counter=`0`、AAGUID 全零、`publicKeyAlgorithm=-48`，並觀測到 challenge/user.id 可能以 hex 傳入。
13. 2026-02-08：已建立根目錄 `extension/` MV3 實作骨架（background/content/injected/options），並通過 `bun run typecheck` 與 `bun run build`。
14. 2026-02-08：`extension/` 新增 bun 測試（M1/M2 核心流程）並通過；同時調整 content script 依 settings 啟用注入、manifest 開放 injected chunk 載入。
15. 2026-02-08：補上 `rpId` 與 `origin` 一致性檢查（trial 採嚴格相等），並新增對應測試案例。
16. 2026-02-08：Signer 改為 provider 架構（`mock` / `wasm-experimental`），新增 `smoke:signer` 腳本；目前 wasm provider 為佔位並回退 mock。
17. 2026-02-08：Storage 升級為 schema 化結構（含 legacy migration），並新增 `store` 測試；同時新增 `smoke:register` 以驗證註冊流程、旗標與 signCount 初值。
18. 2026-02-08：依開發順序將 UV 明確標記為 deferred（暫不實作），當前里程碑專注 key generation + storage + registration flow。
19. 2026-02-08：註冊回應已對齊原生常見欄位：`clientDataJSON.crossOrigin=false`、`clientExtensionResults.credProps`、`transports=[\"internal\"]`。
20. 2026-02-08：移除第三方 PQ JS 套件依賴，改用原生 `liboqs C + wasm` 整合骨架（C bridge + emcc build script + wasm signer provider）。
21. 2026-02-08：CSP 問題修復：MV3 `extension_pages` 加入 `'wasm-unsafe-eval'` 以允許 wasm 編譯/實例化。
22. 2026-02-08：WASI import mismatch 修復：service worker 端補齊 `wasi_snapshot_preview1` imports（含 `random_get`）。
23. 2026-02-08：`credentialPublicKey` COSE mapping 調整為 `kty=7 (AKP)` + `alg=-48/-49/-50` + `-1=pub`，移除 `-70001` marker。
24. 2026-02-08：runtime 改為 wasm-only，移除 mock signer 與 signer provider 分流。
25. 2026-02-08：settings schema 精簡，移除 `signerProvider`；options UI 同步移除 signer selector。
26. 2026-02-08：建置流程新增 `bun run setup` / `bun run build:all`，安裝與建置入口簡化。
27. 2026-02-08：liboqs 建置改為 minimal compile（`SIG_ml_dsa_44/65/87`）以縮短 build 時間。
28. 2026-02-08：測試 refactor：新增 deterministic seeded test utils，移除測試內隨機值依賴，降低 flaky 風險並提升可重現性。
29. 2026-02-08：文件 refactor：擴充 extension README 與各子目錄 README，加入架構資料流、腳本輸入輸出、常見錯誤排查說明。

---

## 11. Spec Artifacts

1. Phase-1 實作規格主檔：`codex/specs/PHASE-1-IMPLEMENTATION-SPEC.md`
2. 目前狀態：`v0.3-draft`（implementation baseline + security backlog tracked）
3. 使用方式：後續所有實作與測試優先對齊此檔，差異需先回寫決策紀錄。

---

## 12. v6 實作同步（本次更新）

### 12.1 Runtime 精簡為 wasm-only

1. 移除 `mock` signer 與 provider 分流，runtime 僅保留 `liboqs wasm` 路徑。
2. `Settings` 移除 `signerProvider` 欄位，options UI 同步移除 signer 選單。
3. Background runtime 固定使用單一 `PQAuthenticator + LiboqsWasmSigner`。

### 12.2 安裝/建置流程優化

新增與調整 scripts：

1. `bun run setup`：一鍵執行 `setup:liboqs:wasm + build:wasm`
2. `bun run build:all`：一鍵執行 `build:wasm + build`
3. 移除 smoke scripts（避免與 wasm-only runtime 目標衝突）

liboqs 編譯優化：

1. `setup-liboqs-emscripten.sh` 改為最小演算法集：
   1. `SIG_ml_dsa_44`
   2. `SIG_ml_dsa_65`
   3. `SIG_ml_dsa_87`
2. 顯著降低 compile 範圍與建置時間。

### 12.3 目錄文件化（README）

已為主要維護目錄新增 README：

1. `extension/public/`
2. `extension/scripts/`
3. `extension/src/`
4. `extension/src/background/`
5. `extension/src/content/`
6. `extension/src/injected/`
7. `extension/src/lib/`
8. `extension/src/options/`
9. `extension/src/types/`
10. `extension/wasm/`
11. `extension/public/wasm/`（更新）

### 12.4 技術棧（明確版）

1. Extension 平台：Chrome MV3（service worker + content script + injected hook）
2. PQ 簽章：`liboqs` C（ML-DSA-44/65/87）
3. WebAssembly：Emscripten 編譯 `pq_bridge.wasm`
4. 前端工具鏈：Vite + React + TypeScript + Bun
5. 儲存：`chrome.storage.local`（schema store）
6. 封包：WebAuthn JSON bridge + base64url binary normalization

### 12.5 已解決的關鍵整合問題

1. CSP wasm 限制：加入 MV3 `content_security_policy`（`wasm-unsafe-eval`）
2. WASI import mismatch：為 `wasi_snapshot_preview1` 補齊 imports（`random_get` 等）
3. COSE key type 不相容：`credentialPublicKey` 改為 `kty=7 (AKP)`，移除 custom marker 欄位
4. 目前狀態：Yubico demo 已可完成 PQ 註冊與 PQ 認證流程（trial baseline）

---

## 13. Security Reports（本次新增）

### 13.1 輸出位置

1. `codex/SECURITY_REPORTS/README.md`
2. `codex/SECURITY_REPORTS/001-PLAIN_PRIVATE_KEY_STORAGE.md`
3. `codex/SECURITY_REPORTS/002-UNTRUSTED_PAGE_TRIGGER_NO_USER_GESTURE.md`
4. `codex/SECURITY_REPORTS/003-MISSING_RUNTIME_SCHEMA_VALIDATION.md`
5. `codex/SECURITY_REPORTS/004-SIGNCOUNT_RACE_CONDITION.md`
6. `codex/SECURITY_REPORTS/005-LIBOQS_UNPINNED_SOURCE_SUPPLY_CHAIN.md`
7. `codex/SECURITY_REPORTS/006-PRODUCTION_SOURCEMAP_EXPOSURE.md`
8. `codex/SECURITY_REPORTS/007-CSP_AND_RESOURCE_SURFACE_MINIMIZATION.md`

### 13.2 本輪策略

1. `UV` 報告依決策暫緩（排到最後階段），本輪不納入獨立檔。
2. 先聚焦可立即落地的修補面：
   1. key material storage
   2. message boundary validation
   3. 操作確認（user intent gate）
   4. signCount 競態保護

### 13.3 命名檢討（spec）

1. `M1-M2-SPEC-FREEZE` 對現況已不夠精準。
2. 目前已超過單純 M1/M2 freeze，已包含 implementation baseline 與安全追蹤。
3. 已完成改名為：`codex/specs/PHASE-1-IMPLEMENTATION-SPEC.md`，舊檔已移除。

### 13.4 Decision Log 增補

30. 2026-02-08：新增 `codex/SECURITY_REPORTS/*.md` 一議題一檔安全報告，作為後續修補與教學素材。
31. 2026-02-08：`UV` 安全議題明確列為 deferred（最後階段處理），避免干擾現階段 refactor + audit 主線。
32. 2026-02-08：spec 已完成命名遷移為 `PHASE-1-IMPLEMENTATION-SPEC`，`M1-M2-SPEC-FREEZE` 舊檔已移除。
33. 2026-02-08：實作 `native-touch-id` UV 路徑（extension background 透過 Native Messaging 呼叫 macOS Touch ID host，失敗即中止 create/get）。
34. 2026-02-08：新增 native host 程式：`extension/native-host/pq_uv_host.swift`（支援 `uv-request` 與 `uv-status`）。
35. 2026-02-08：新增 macOS 腳本：`build-native-host-macos.sh`、`install-native-host-macos.sh`、`setup-touch-id-uv-macos.sh`（一鍵 build+install）。
36. 2026-02-08：options UI 新增 `uvMode = native-touch-id` 與 native host 狀態面板（ready/not-ready、refresh、detail）。
37. 2026-02-08：manifest 新增 `nativeMessaging` 權限；README 與 scripts README 已同步 Touch ID 安裝流程。
38. 2026-02-08：修正 native host 編譯問題：移除錯誤 `fflush(FileHandle)` 用法；build 腳本加上 `-module-cache-path` 與 `-sdk` 以降低 toolchain/權限問題。
39. 2026-02-08：確認目前流程策略：預設可無 UV 正常註冊/認證；需要硬體 UV 的使用者再安裝 native host（後續擴充 Windows Hello）。

---

## 14. 今日進度同步（Touch ID UV）

### 14.1 已完成

1. UV 機制：
   1. `soft-auto`（預設，無 native host 也可用）
   2. `native-touch-id`（需 native host，Touch ID 驗證成功才放行）
2. Native Messaging bridge：
   1. host 不存在/中斷/逾時皆回 `NotAllowedError`
   2. 錯誤訊息提供可操作指引（安裝腳本、allowlist 不符等）
3. Native host 狀態檢查：
   1. 新增 `PQ_UV_STATUS` message channel
   2. host 支援 `uv-status` 快速回報 `ready/version/platform`
4. 安裝體驗：
   1. 一鍵命令：`bun run setup:touch-id:macos -- <CHROME_EXTENSION_ID>`
   2. 手動最後步驟：reload extension + options 切換 `native-touch-id`

### 14.2 目前驗證狀態

1. `bun run typecheck`：pass
2. `bun run test`：pass
3. `bun run build`：pass
4. `bun run build:native-host:macos`：pass（修正後）

### 14.3 發佈與平台策略（確認）

1. 僅安裝 extension（`dist`）時，仍可在 `soft-auto` 模式正常使用（無硬體 UV）。
2. 若要 Touch ID/Windows Hello 等硬體 UV，使用者仍需安裝對應 native host（Chrome 安全模型限制，extension 無法靜默安裝）。
3. 下一階段可沿用同一 `uv-request/uv-result/uv-status` 協定擴充 Windows Hello host。

### 14.4 明日後續

1. 進入安全性更新階段（依 `codex/SECURITY_REPORTS/*.md` 項目逐步處理）。
2. UV 主線先維持可用狀態，不在本輪引入大規模重構。

---

## 15. FN-DSA 整合階段（2026-11）

每日計畫見 `codex/FN-DSA-PLAN.md`，每天的細節見 `codex/worklog/`。

### 15.1 Decision Log 增補

40. 2026-11-13：查證標準現況。ML-DSA 依 FIPS 204（2024-08-13）；COSE 編號 -48/-49/-50 與 AKP 金鑰類型（kty = 7）已由 RFC 9964 正式登記。專案的 ML-DSA 實作符合標準（liboqs `ML-DSA-44/65/87`、pure ML-DSA、context 為空字串）。
41. 2026-11-13：FN-DSA 依 Falcon 原作者提交給 NIST 的第三輪規格 v1.2（2020-10-01）實作，使用 liboqs 的 Falcon-512/1024，官方 KAT 100/100 筆逐 byte 一致。FIPS 206 尚未發布，NIST 已公告將修改原規格，正式版發布後需要遷移並重新註冊憑證。
42. 2026-11-13（D1）：FN-DSA-512 = -54、FN-DSA-1024 = -55，標示為暫定；這兩個編號是 draft-ietf-cose-falcon-04 申請中的值，IANA 尚未分配。
43. 2026-11-13（D2）：liboqs 變體採用 `Falcon-512`／`Falcon-1024`（不補滿格式，與官方 KAT 相同）。
44. 2026-11-13（D3）：建立共用演算法表 `shared/pq-algorithms.json`，Python 與 TypeScript 讀同一份，C bridge 以測試檢查一致性。
45. 2026-11-13（D4）：WASM 端的 liboqs 固定在 commit 33815beb，不再追 `main`；Python 端維持 liboqs 0.14.0。
46. 2026-11-13（D5）：Extension 在開發時允許 `http://localhost:3000`，以便用本機 RP 做 FN-DSA 端到端測試。
47. 2026-11-13（D6）：RP 預設宣告順序為 `[-49, -48, -50, -54, -55]`，維持 ML-DSA 優先。
48. 2026-11-13：工作流程改為每個 Day 一個 `day-NN` 分支，commit 訊息格式為 `Day N: …`，PR 由使用者在 GitHub 合併。
49. 2026-11-16：建立專案守則 `CLAUDE.md`：語言與註解、每日流程、TDD 與避免球員兼裁判的六項措施、每次 commit 前必跑的檢查、GitHub Actions CI。
50. 2026-11-16：新增協議導覽 `codex/PROTOCOL-GUIDE.html`，名詞表以導覽第 11 章為唯一版本。
51. 2026-11-16：RP 登入驗章改用收到的 clientDataJSON 原始 bytes 計算雜湊（WebAuthn §7.2），不再解析後重新序列化。
52. 2026-11-16：Python authenticator 的 allowCredentials 只從清單中挑選屬於目前 rpId 的憑證，挑不到就拒絕（Phase-1 spec 6.2）。
53. 2026-11-16：Python authenticator 缺少 origin 時直接回報錯誤，不自動填入預設值。
54. 2026-11-16：Python authenticator 的 credential ID 必須完全相同才算同一張憑證。儲存層只接受 base64url 字元組成的 ID，讀出檔案後再比對檔案內記錄的 ID，避免 Windows 檔名不分大小寫、或 `../` 這類路徑讓清單以外的憑證被選中（WebAuthn §6.3.2、§6.3.3）。
55. 2026-11-16：Python bridge 的 origin 改取自 Playwright 提供的呼叫者 frame 網址，只取協定、網域、埠，不再採用頁面在 payload 中自稱的值（WebAuthn §5.8.1：origin 由瀏覽器填入，網頁無法指定）。
56. 2026-11-16：使用者決定 Day 1 最後三個 commit（`e19f74a`、`3486103`、`2ba3d1f`）例外，commit 前只跑 ruff 與新增的 T12、T13，全套測試交給 PR 上的 CI。`CLAUDE.md` 的通用規則不變。
57. 2026-11-17：共用演算法表的 Python 讀取模組放在 `shared/pq_algorithms.py`，測試放在 `shared/tests/`。RP 與 authenticator 在協議中是不同角色，彼此不 import 對方的程式碼，共用的定義放在中立的 `shared/`。
58. 2026-11-17：共用演算法表的 `status` 表示 COSE 編號是否已正式分配：`standard`（IANA 已分配，ML-DSA）或 `provisional`（IETF 草案暫定，FN-DSA），不採用交接文件的 `stable in repo`／`planned`。另新增 `signatureLengthFixed`，標明 FN-DSA 的 `signatureBytes` 是上限而不是固定長度。
59. 2026-11-17：RP 與 authenticator 的 COSE → liboqs 對照從 Day 2 起改由共用演算法表產生，FN-DSA -54/-55 隨之對兩端生效；RP 的 `hosted_algorithms` 不變，宣告與註冊仍只限 ML-DSA，Day 3 才開放。
60. 2026-11-18：RP 的 `hosted_algorithms` 預設改為 `[-49, -48, -50, -54, -55]`（依 D6），宣告並接受 FN-DSA。註冊時另外要求 COSE_Key 的 kty 為 7（AKP，RFC 9964），公鑰長度等於共用演算法表的 `publicKeyBytes`，不符回 400 `Invalid public key`；長度錯的公鑰若存進 DB，登入時太短會驗章失敗，太長會讓 liboqs-python 丟出 `ValueError`（500）。
61. 2026-11-18：Python authenticator 註冊時先選演算法、再做使用者驗證（WebAuthn §6.3.2 第 2 步先於第 6 步）。RP 給的演算法都不支援時直接拒絕，不跳出 Windows Hello。excludeCredentials 維持在使用者驗證之後，規格要求先取得使用者同意才回「重複」，避免網站在使用者不知情時探測裝置上的憑證。
62. 2026-11-23：前端只在 RP 發出的 `pubKeyCredParams` 內重排：選單選的演算法移到第一個，其他保持原順序；RP 沒宣告時前端顯示錯誤並停止，不呼叫 `navigator.credentials.create`（WebAuthn §5.4，前端不替 RP 增加演算法）。前端選單自己保留一份清單，由 bun 測試比對 `shared/pq-algorithms.json`，不直接 import（避免修改 Next.js 建置設定）。跨元件整合測試放在 `tests/integration/`，`tests` 一併加入 pytest `testpaths`、CI 與 `CLAUDE.md` 的 ruff 路徑（使用者同意修改 `CLAUDE.md`）。
63. 2026-11-24：保留 Extension 的 FN-DSA（Day 6–9），不改成只做 Playwright 路線。Playwright 路線是先在 Yubico 上證明可行的原型，Extension 是給一般使用者的成品（2026-02-07 決策）。目前沒有公開的 RP 宣告 -54/-55，FN-DSA 只能用本機 RP 展示，展示分三個場景：Yubico 上的 ML-DSA（和別人的 RP 互通）、本機 RP 上的 FN-DSA、本機 RP 不宣告 FN-DSA 時 Extension 不選它。Extension 的簽章由 WASM 版 liboqs 產生、RP 的 Python liboqs 驗章，等於兩份分別編譯的實作互相驗證。
