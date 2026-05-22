**目標任務**
把目前只支援：

- `ML-DSA-44 -> -48`
- `ML-DSA-65 -> -49`
- `ML-DSA-87 -> -50`

擴充成支援：

- `FN-DSA-512 -> -54 -> Falcon-512`
- `FN-DSA-1024 -> -55 -> Falcon-1024`

重點不是改畫面，而是讓 **RP Server、Python Authenticator、Chrome Extension、WASM bridge、測試** 對同一組 COSE `alg` 有一致解讀。

**Feature 工作表**
| 優先 | Feature | 目的 | 主要任務 | 驗收標準 |
|---|---|---|---|---|
| P0 | F01：固定 FN-DSA 演算法規格 | 先定義共識，避免後面 mapping 分散 | 確認 `FN-DSA-512=-54`、`FN-DSA-1024=-55`；確認 liboqs 實作名稱仍是 `Falcon-512/1024`；確認 byte sizes | 文件、程式、測試都只用 `-54/-55` 表示 FN-DSA |
| P0 | F02：建立 shared algorithm registry | 建立單一真實來源 | 建立共用演算法表，欄位含 `label/coseAlg/oqsName/publicKeyBytes/privateKeyBytes/signatureBytes/status` | 後續 RP、authenticator、extension 不再各自硬寫 mapping |
| P0 | F03：RP Server 支援 FN-DSA 宣告 | 讓 RP 可以在註冊 options 宣告 FN-DSA | 更新 `hosted_algorithms`；確認 `/register/options` 輸出 `-54/-55`；更新 `COSE_TO_OQS` | RP 回傳的 `pubKeyCredParams` 包含 `-54/-55` |
| P0 | F04：RP Server 支援 FN-DSA 驗章 | 讓 RP 註冊與登入都能驗 FN-DSA | 註冊時允許 `credentialPublicKey[3]` 為 `-54/-55`；登入時用 DB 的 algorithm 找到 `Falcon-*` verifier | FN-DSA credential 可被存入 DB，assertion 可驗章成功 |
| P0 | F05：Python Authenticator 支援 FN-DSA keygen/sign | 先跑通最小核心流程 | 更新 COSE → OQS mapping；確認 `PQCSignatureSuite(-54/-55)` 可產 keypair/sign | Python authenticator 能選 `-54/-55` 並產出簽章 |
| P0 | F06：Python WebAuthn COSE_Key 相容性確認 | 確認不用重寫 WebAuthn binary 結構 | 檢查 `credentialPublicKey` 是否仍為 `{1:7, 3:alg, -1:pubkey}` | `credentialPublicKey[3]` 可正確放入 `-54/-55` |
| P1 | F07：Chrome Extension 型別支援 FN-DSA | 讓 extension TypeScript 層接受新 alg | 更新 `SupportedAlg`；更新 settings/default algorithm 型別；更新 options UI 選項 | TypeScript 不再拒絕 `-54/-55` |
| P1 | F08：Extension authenticator 選演算法支援 FN-DSA | 讓 extension 能根據 RP request order 選 FN-DSA | 更新 `SUPPORTED_ALGORITHMS`、`toSupportedAlg()`、`selectAlgorithm()` | `pubKeyCredParams=[-7,-54]` 時會選 `-54` |
| P1 | F09：Extension COSE public key 支援 FN-DSA | 讓 attestationObject 內的 COSE_Key 正確 | 確認 `credentialPublicKeyCose()` 不需改結構，只需允許 alg | attestation 解析後 `credentialPublicKey[3] === -54/-55` |
| P1 | F10：Extension key/signature byte-size constants | 避免 sign/keygen 長度錯誤 | 更新 `PUBLIC_KEY_BYTES`、`PRIVATE_KEY_BYTES`、`SIGNATURE_BYTES` | FN-DSA keypair/signature buffer 長度正確 |
| P1 | F11：WASM bridge 支援 Falcon | 讓 extension 真正能呼叫 liboqs Falcon | 更新 `pq_alg_name()`：`-54 -> Falcon-512`、`-55 -> Falcon-1024` | WASM C bridge 能建立 Falcon signer |
| P1 | F12：liboqs wasm build 加入 Falcon | 讓編譯出的 wasm 包含 Falcon | 更新 minimal build 清單，加入 Falcon-512/1024 | `pq_bridge.wasm` 可查詢 FN-DSA key/signature length |
| P1 | F13：演算法選擇測試 | 防止 RP/authenticator 對 alg 解讀不一致 | 測 `[-54]`、`[-55]`、`[-7,-54]`、不支援 alg | request order 正確，無支援 alg 時拒絕 |
| P1 | F14：註冊流程測試 | 驗證 makeCredential | 測 `attestationObject`、`credentialPublicKey[3]`、storage/DB algorithm | 註冊後保存 `algorithm=-54/-55` |
| P1 | F15：登入流程測試 | 驗證 getAssertion | 測 assertion message、signature verify、signCount | FN-DSA assertion 可被對應公鑰驗章 |
| P1 | F16：負向測試 | 防止 authenticator 私自選 FN-DSA | RP 未宣告 `-54/-55` 時，authenticator 不可選 FN-DSA | 嚴格遵守 RP `pubKeyCredParams` |
| P2 | F17：端到端驗證 | 確認整條鏈路可用 | RP + frontend + authenticator/extension 完整跑 register/authenticate | `-54` 和 `-55` 至少各跑一次成功路徑 |
| P2 | F18：文件同步 | 避免交接漂移 | 更新 spec、REPORTS、README、handover 實作狀態 | 文件與程式支援狀態一致 |
| P2 | F19：安全 backlog 檢視 | 不阻塞 FN-DSA，但要記錄風險 | 私鑰儲存、user gesture、schema validation、signCount race 等另列後續 | 不把安全 backlog 混進 FN-DSA MVP |

**建議工作流程**
1. 先做 `F01-F02`  
   這是地基。沒有 shared registry，後面很容易出現 RP 支援了 `-54`，但 extension/wasm 還不知道它是 `Falcon-512`。

2. 再做 `F03-F06`  
   先讓 **RP + Python Authenticator** 跑通，這符合 handover 的推薦順序，也是最快驗證協定理解是否正確的方式。

3. 接著做 `F07-F12`  
   再把同一套能力搬到 Chrome extension / wasm。這部分成本較高，尤其是 liboqs wasm build。

4. 然後做 `F13-F16`  
   先補小測試，不急著 E2E。FN-DSA 這類 mapping 工作最怕「看起來都有加，實際某層漏掉」。

5. 最後做 `F17-F18`  
   跑完整 register/authenticate，再同步文件。

**MVP 必須完成**
如果我們要定義「這週真正要完成」的最小版本，我會抓這些：

- `F01` 固定 `-54/-55`
- `F02` shared registry
- `F03-F04` RP 支援宣告與驗章
- `F05-F06` Python authenticator 支援 keygen/sign/COSE
- `F07-F12` extension/wasm 支援 FN-DSA
- `F13-F16` 最小測試
- `F17` 至少跑通 `FN-DSA-512 (-54)` E2E

`FN-DSA-1024 (-55)` 最好也 E2E，但如果時間卡在 wasm build 或效能，至少要完成 mapping + unit tests。