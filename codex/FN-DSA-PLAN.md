# FN-DSA（Falcon Round 3）整合實作計畫

| 項目 | 內容 |
|---|---|
| 建立日期 | 2026-11-13 |
| 分支 | `feature/fn-dsa-integration`（從 `main` 49247e0 切出） |
| 依據 | [workflow.md](../workflow.md)、[FALCON_INTEGRATION_HANDOVER.md](docs/FALCON_INTEGRATION_HANDOVER.md) |
| 工作量 | 每天約 3 小時，共 12 天（Day 1–Day 12） |
| 狀態 | 已確認（第 3 節的設計決策 D1–D6 已於 2026-11-13 確認） |

---

## 1. 目標與範圍（Clarify）

### 目標
讓 RP Server、Python Authenticator、Chrome Extension、WASM bridge 都支援：

| 名稱 | COSE alg | liboqs 名稱 |
|---|---:|---|
| FN-DSA-512 | -54 | `Falcon-512` |
| FN-DSA-1024 | -55 | `Falcon-1024` |

並完成「Python bridge」與「Chrome Extension」兩條路線的註冊 + 登入端到端流程。

### 實作依據
- 演算法：Falcon 原作者提交給 NIST 的第三輪規格 **Specification v1.2（2020-10-01）**，透過 liboqs 實作。
- **不是** FIPS 206：NIST 尚未發布 FIPS 206，而且已公告會修改原規格（BUFF transform、公鑰改 NTT 形式、只准定點數運算等），未來需要遷移。

### 不在範圍內
- FIPS 206 正式版（尚未發布）
- 在 demo.yubico.com 上測試 FN-DSA（該 RP 不宣告 -54/-55）
- 安全 backlog 的修補（只檢視與記錄，見 F19）

---

## 2. 已確認的事實（2026-11-13 查證）

| 項目 | 結論 |
|---|---|
| liboqs 是否符合原作者規格 | 符合。liboqs 0.14.0 的 Falcon-512/1024 與官方提交包 `Falcon-Round3.zip` 內的 KAT 100/100 筆逐 byte 一致 |
| 金鑰與簽章大小 | 公鑰 897 / 1793 bytes；私鑰 1281 / 2305 bytes；簽章長度**不固定**，上限 752 / 1462 bytes（padded 版固定 666 / 1280） |
| 簽章格式 | `Falcon-512` 為不補滿格式（規格書 3.11.6，與官方 KAT 相同）；`Falcon-padded-512` 為補滿格式（規格書 3.11.3）。兩者金鑰相同，可互相驗證 |
| COSE 編號 | -54/-55 是 draft-ietf-cose-falcon-04 **申請中**的編號，IANA 尚未分配，屬暫定 |
| COSE_Key 結構 | 沿用 `{1: 7 (AKP), 3: alg, -1: 公鑰}`，不需改結構 |
| Python 端 liboqs | 原生 liboqs 0.14.0（`C:\Users\user\_oqs`）+ liboqs-python 0.14.1，已內建 Falcon |
| WASM 端 liboqs | 原始碼在 `extension/.deps`，版本為 `main` @ 33815beb（0.15.0 之後），目前只編譯 ML-DSA |
| 既有測試基準 | Python 14 個、Extension 11 個、Frontend 4 個，全部通過 |

---

## 3. 設計決策（2026-11-13 已確認）

| 編號 | 決策 | 理由 |
|---|---|---|
| D1 | FN-DSA-512 = -54、FN-DSA-1024 = -55，狀態標示為暫定 | 與 IETF 草案申請的編號一致；正式分配前可能變動 |
| D2 | 使用 liboqs `Falcon-512` / `Falcon-1024`（不補滿格式） | 交接文件既定，且與官方 KAT 格式相同；改用 padded 版也符合規格 |
| D3 | 建立共用演算法表 `shared/pq-algorithms.json`，Python 與 TypeScript 讀同一份；C bridge 用測試檢查一致性 | 避免 mapping 分散在各層，以後切換到 FIPS 206 只改一個地方 |
| D4 | WASM 端的 liboqs 固定在目前的 commit 33815beb，不再追 `main`；Python 端維持 0.14.0 | 避免重建時 ML-DSA 行為改變；兩端的 Falcon 程式碼相同 |
| D5 | Extension 在開發時允許 `http://localhost:3000` | Yubico demo 不宣告 FN-DSA，只能用本機 RP 做端到端測試 |
| D6 | RP 預設宣告順序為 `[-49, -48, -50, -54, -55]` | 維持 ML-DSA 優先，既有行為不變；測試時可改設定只留 FN-DSA |

---

## 4. 每日計畫（Plan）

### 每天 3 小時的進行方式
1. 約 15 分鐘：回顧前一天、確認今天的目標
2. 約 2 小時：實作（Claude 寫程式，你審閱並提問）
3. 約 30 分鐘：跑測試、commit
4. 約 15 分鐘：更新本文件的勾選狀態

### Day 0｜11/13：準備（已完成）
- [x] 建立分支 `feature/fn-dsa-integration`
- [x] 撰寫本計畫

### Day 1｜11/14：前置修正
- [ ] 在 `pyproject.toml` 設定 pytest 的 `testpaths`（0.5h）
  - 原因：在根目錄直接跑 `pytest` 會掃到並執行 `extension/emsdk` 內第三方套件的範例程式（2026-11-13 曾因此在根目錄產生 `test_localsystem.txt`）
- [ ] RP 驗章改用收到的原始 `clientDataJSON` bytes 計算 hash，並補測試（1h）
- [ ] Python authenticator：`allowCredentials` 比對不到時回傳錯誤（符合 Phase-1 spec 6.2），並補測試；修正不存在的 `self.settings.origin`（1h）
- [ ] 在 `codex/REPORTS.md` 的 Decision Log 補記 D1–D6（0.5h）

**完成標準**：所有既有測試通過，ML-DSA 行為不變。

### Day 2｜11/15：F01 + F02 共用演算法表
- [ ] 建立 `shared/pq-algorithms.json`，五個演算法的欄位：`label`、`coseAlg`、`oqsName`、公鑰／私鑰／簽章大小、簽章長度是否固定、`status`（1h）
- [ ] Python 讀取模組，RP 與 authenticator 共用（1h）
- [ ] 測試：表內大小等於 liboqs 實際大小；COSE 編號不重複（1h）

**完成標準**：Python 兩端的 mapping 都改從共用表讀取，既有測試通過。

### Day 3｜11/16：F03 + F04 RP Server
- [ ] `hosted_algorithms` 加入 -54/-55（0.5h）
- [ ] 註冊時允許 `credentialPublicKey[3]` 為 -54/-55，驗章時從共用表取得 liboqs 名稱（1h）
- [ ] 測試：`/register/options` 包含 -54/-55；FN-DSA 憑證可存入 DB 並驗章成功（1.5h）

**完成標準**：RP 能宣告、接受並驗證 FN-DSA。

### Day 4｜11/17：F05 + F06 + F16 Python Authenticator
- [ ] COSE → liboqs 對應改用共用表，-54/-55 可產生金鑰與簽章（1h）
- [ ] 確認產生的 `credentialPublicKey` 為 `{1: 7, 3: -54, -1: 公鑰}`（0.5h）
- [ ] 測試：`[-54]`、`[-55]`、`[-7, -54]` 的選擇結果；不支援時拒絕；RP 沒宣告 FN-DSA 時不得選用（1.5h）

**完成標準**：authenticator 嚴格依照 RP 的 `pubKeyCredParams` 選擇演算法。

### Day 5｜11/18：Python 路線整合 + 前端
- [ ] pytest 整合測試：authenticator ↔ RP 完整註冊 + 登入，五種演算法都跑（1.5h）
- [ ] 前端選單加入 FN-DSA；排序只在 RP 有宣告的演算法中進行（目前會把使用者選的演算法硬塞到最前面）（1h）
- [ ] 手動端到端：-54、-55 各跑一次註冊 + 登入，並檢查 DB 的 `algorithm` 欄位（0.5h）

**完成標準**：Python bridge 路線的 FN-DSA 端到端成功（F17 前半）。

### Day 6｜11/19：F07–F10 Extension TypeScript 層
- [ ] `SupportedAlg` 型別、設定、options 選單加入 -54/-55（1h）
- [ ] `SUPPORTED_ALGORITHMS`、`toSupportedAlg()`、`selectAlgorithm()`、長度常數改用共用表（1h）
- [ ] bun 測試：`[-7, -54]` 選到 -54；`credentialPublicKey[3] === -54`；簽章長度以上限處理（1h）

**完成標準**：TypeScript 型別檢查與 bun 測試通過。

### Day 7｜11/20：F11 + F12 WASM
- [ ] `pq_bridge.c` 加入 -54 → `Falcon-512`、-55 → `Falcon-1024`（0.5h）
- [ ] 編譯清單加入 `SIG_falcon_512;SIG_falcon_1024`，`LIBOQS_REF` 固定版本（0.5h）
- [ ] 重建 `liboqs.a`、`pq_bridge.wasm` 與 extension（1h）
- [ ] 確認 WASM 回報的金鑰與簽章大小正確；ML-DSA 既有測試仍通過（1h）

**完成標準**：`pq_bridge.wasm` 可產生 Falcon 金鑰與簽章。

### Day 8｜11/21：Extension 開放 localhost + WASM KAT
- [ ] manifest 與 `isTrustedSender()` 開放 `http://localhost:3000`（僅開發用）（1h）
- [ ] WASM 版 Falcon 跑官方 KAT 比對（2h）

**完成標準**：WASM 版 Falcon 與官方 KAT 一致。

### Day 9｜11/22：Extension 路線端到端（F17 後半）
- [ ] 載入 extension，對本機 RP 跑 -54、-55 的註冊 + 登入（2h）
- [ ] 檢查 `chrome.storage` 與 DB 的 `algorithm`（1h）

**完成標準**：Extension 路線的 FN-DSA 端到端成功。

### Day 10｜11/23：F13–F16 測試補強
- [ ] 官方 KAT 測試納入專案（只存雜湊值，不放 3 MB 的 KAT 檔）（1.5h）
- [ ] 補齊缺少的選擇／註冊／登入／負向測試，跑全部測試（1.5h）

**完成標準**：workflow.md F13–F16 的驗收標準都有對應測試。

### Day 11｜11/24：F18 文件同步 + F19 安全 backlog
- [ ] 同步 README、交接文件、`codex/REPORTS.md`、`codex/ARCHITECTURE_EXPLAINED.md`（2h）
- [ ] 檢視安全 backlog，記錄 FN-DSA 相關風險（1h）

**完成標準**：文件與程式的支援狀態一致。

### Day 12｜11/25：緩衝與收尾
- [ ] 回歸測試：ML-DSA 與 FN-DSA、兩條路線都跑一次（1.5h）
- [ ] 整理 commit，討論是否開 PR 合併回 `main`（1.5h）

> 若某天進度落後就整體順延。以 2027 年 3 月前的期限來看，仍有充足緩衝。

---

## 5. 修改點總覽（Interface）

| 層 | 檔案 | 修改內容 |
|---|---|---|
| 共用 | `shared/pq-algorithms.json`（新增） | 演算法表，唯一的資料來源 |
| 設定 | [pyproject.toml](../pyproject.toml) | pytest `testpaths` |
| RP | [rp_server/config.py](../rp_server/config.py) | `hosted_algorithms` |
| RP | [rp_server/services.py](../rp_server/services.py) | 改用共用表；原始 bytes 計算 hash |
| Authenticator | [authenticator/pqcrypto.py](../authenticator/pqcrypto.py) | 改用共用表 |
| Authenticator | [authenticator/service.py](../authenticator/service.py) | `allowCredentials` 行為；`origin` 修正 |
| Frontend | [frontend/src/pages/index.tsx](../frontend/src/pages/index.tsx) | 選單與排序邏輯 |
| Extension | [extension/src/types/messages.ts](../extension/src/types/messages.ts) | `SupportedAlg` |
| Extension | [extension/src/background/authenticator.ts](../extension/src/background/authenticator.ts) | 演算法選擇 |
| Extension | [extension/src/background/pq-signer.ts](../extension/src/background/pq-signer.ts) | 長度常數 |
| Extension | [extension/src/background/index.ts](../extension/src/background/index.ts)、[extension/public/manifest.json](../extension/public/manifest.json) | 開放 localhost |
| Extension | [extension/src/options/App.tsx](../extension/src/options/App.tsx) | 選單 |
| WASM | [extension/wasm/pq_bridge.c](../extension/wasm/pq_bridge.c) | COSE → Falcon 名稱 |
| WASM | [extension/scripts/setup-liboqs-emscripten.sh](../extension/scripts/setup-liboqs-emscripten.sh) | 編譯清單、固定版本 |

---

## 6. 風險與對策（Risk）

| 風險 | 影響 | 對策 |
|---|---|---|
| WASM 在 Windows 上重建失敗 | F12 卡關 | 5/30 曾成功建置，工具都還在；不行就改用 WSL 或 Docker |
| 重建 liboqs 讓 ML-DSA 行為改變 | 既有功能壞掉 | 固定 liboqs 版本（D4）；重建後跑既有測試與 ML-DSA 端到端 |
| Extension 讀不到 repo 根目錄的共用表 | D3 無法直接套用 | 改成建置時從 JSON 產生 TS 檔 |
| Falcon 簽章長度不固定 | 長度常數用錯 | 一律當作上限處理，並加測試 |
| 開放 localhost 擴大 extension 的攻擊面 | 安全性降低 | 只用於開發，文件記錄（參考安全報告 007） |
| 未來 FIPS 206 與現在的實作不相容 | 需要遷移、重新註冊 | `status` 標示暫定；KAT 測試偵測變化；報告寫明 |
| Windows Hello 每次操作都會跳出 | 自動化測試麻煩 | 自動化測試使用 `NoopVerifier` |

---

## 7. 完成標準（Definition of Done）

- [ ] -54 與 -55 在 Python bridge、Chrome Extension 兩條路線都完成註冊 + 登入
- [ ] 既有測試與新增測試全部通過
- [ ] 官方 KAT 測試納入專案（Python 與 WASM）
- [ ] 文件標明：依 Falcon 第三輪規格實作、-54/-55 為暫定編號、FIPS 206 發布後需遷移

---

## 8. 分支與提交方式

- 所有工作都在 `feature/fn-dsa-integration` 上進行
- 每完成一個項目就 commit 一次，訊息標註 F 編號，例如 `feat(rp): verify FN-DSA assertions (F03-F04)`
- 推送到遠端或開 PR 前先討論確認

---

## 9. 參考資料

- [Falcon Specification v1.2](https://falcon-sign.info/falcon.pdf)
- [NIST Round 3 Submissions（Falcon-Round3.zip）](https://csrc.nist.gov/Projects/post-quantum-cryptography/post-quantum-cryptography-standardization/round-3-submissions)
- [draft-ietf-cose-falcon-04](https://www.ietf.org/archive/id/draft-ietf-cose-falcon-04.html)
- [NIST：FIPS 206 Status Update（2025）](https://csrc.nist.gov/csrc/media/Presentations/2025/fips-206-fn-dsa-(falcon)/images-media/fips_206-perlner_2.1.pdf)
- [NIST pqc-forum：New plan for FN-DSA（2026-09-28）](https://groups.google.com/a/list.nist.gov/g/pqc-forum/c/7z-y5qp-W2Y/m/a11CmUsuBQAJ)
- [RFC 9964：ML-DSA for JOSE and COSE](https://www.rfc-editor.org/rfc/rfc9964.html)
