# FN-DSA 整合交接報告

日期：2026-03-04

## 1. 文件目的

接手此專案時，請先掌握以下三件事：

1. 目前這個 PoC 怎麼把 PQ 簽章演算法接進 WebAuthn / FIDO2 流程。
2. 如果未來要新增 `FN-DSA-512` 與 `FN-DSA-1024`，應該改哪些層。
3. 實作時應如何統一使用 COSE algorithm id `-54` 與 `-55`。

本文整理的是背景、設計與整合 SOP，不包含實作程式碼。

## 2. 先講結論

### 2.1 專案目前的狀態

這個 repo 目前正式接好的 PQ 簽章演算法是：

1. `ML-DSA-44` -> COSE `-48`
2. `ML-DSA-65` -> COSE `-49`
3. `ML-DSA-87` -> COSE `-50`

整個流程的核心做法是：

1. RP Server 在 `pubKeyCredParams` 宣告它接受哪些 `alg`。
2. Authenticator 從 RP 提供的 `alg` 清單中選擇一個自己支援的演算法。
3. Authenticator 產生公私鑰，將公鑰包成 `credentialPublicKey` 的 COSE_Key，並把 `alg` 一起放進 attestation。
4. RP Server 在註冊時把 `algorithm` 與 `public_key` 存起來。
5. RP Server 在驗證 assertion 時，根據 DB 裡紀錄的 `algorithm` 決定要用哪個 PQ verifier。

後續若要整合 `FN-DSA`，重點不是改前端畫面，而是讓 RP、Authenticator、Verifier 三邊對同一組 COSE `alg` 有一致解讀。

### 2.2 FN-DSA 的交接基準

本專案後續交接與整理一律採用以下對應：

1. `FN-DSA-512` -> COSE `-54`
2. `FN-DSA-1024` -> COSE `-55`

也就是說，之後的專案文件、mapping 表、測試案例與 SOP，都以 `FN-DSA` 和 `-54/-55` 為主軸，不再混用其他命名方式。

## 3. 目前 repo 裡，演算法是怎麼被串起來的

### 3.1 RP Server

RP 端負責兩件事：

1. 在 `/register/options` 回傳 `pubKeyCredParams`
2. 在 `/register/verify` / `/authenticate/verify` 依 `algorithm` 做驗證

目前對應落點：

1. `rp_server/config.py`
   `hosted_algorithms` 決定 RP 會對外宣告哪些演算法。
2. `rp_server/app.py`
   把 `hosted_algorithms` 轉成 `pubKeyCredParams` 回給前端。
3. `rp_server/services.py`
   - 註冊時從 `credentialPublicKey[3]` 取出 `alg`
   - 驗證 `alg` 是否在 `hosted_algorithms`
   - 用 `COSE_TO_OQS` 把 COSE id 映射到 `oqs.Signature(...)` 要用的名字

### 3.2 Python authenticator

Python authenticator 的責任是：

1. 依 RP 指定的演算法產生 keypair
2. 把公鑰包成 `credentialPublicKey`
3. 用對應演算法對 assertion message 做簽章

目前對應落點：

1. `authenticator/pqcrypto.py`
   COSE id -> `oqs` 演算法名稱
2. `authenticator/webauthn.py`
   建立 `credentialPublicKey` 的 COSE 結構

這裡現在的 COSE_Key 結構是：

```text
{
  1: 7,         # kty = AKP
  3: alg,       # COSE algorithm id
  -1: pubkey    # raw public key bytes
}
```

這個做法與 FN-DSA 的 COSE 表示方向相容，所以整合 `FN-DSA` 時，通常不需要重寫 `credentialPublicKey` 結構，而是補齊新的演算法 mapping。

### 3.3 Chrome extension 路線

若後續維護的是 extension 版 authenticator，還要同步確認以下幾層：

1. `extension/src/types/messages.ts`
   `SupportedAlg` 型別目前只接受 `-48/-49/-50`
2. `extension/src/background/authenticator.ts`
   `SUPPORTED_ALGORITHMS`、`toSupportedAlg()`、`credentialPublicKeyCose()`
3. `extension/src/background/pq-signer.ts`
   每種演算法的 `publicKey/privateKey/signature` byte 長度
4. `extension/wasm/pq_bridge.c`
   COSE id -> `OQS_SIG_new(...)` 的名稱映射

## 4. 名稱整理方式

為了避免名稱混亂，文件與口頭交接一律統一使用：

1. `FN-DSA-512`
2. `FN-DSA-1024`

只有在說明底層 PQ library 時，才補充以下一句：

> 目前這個專案環境中的 `liboqs` 仍使用 `Falcon-512` 與 `Falcon-1024` 作為實作名稱，所以程式裡可能會看到 `FN-DSA` 的 COSE id 對到 `Falcon-*` 的 `oqs` 名稱。

也就是說，實務上有兩層名稱：

1. 協定與文件層：`FN-DSA-512` / `FN-DSA-1024`
2. `liboqs` 實作層：`Falcon-512` / `Falcon-1024`

交接時以前者為主，後者只作為實作細節。

## 5. 推薦的整合方式

### 5.1 建立單一真實來源的演算法表

不要把 mapping 分散在各個檔案硬寫。應先定義一份表，讓所有層都從這份表延伸。

建議表格至少包含：

| label | coseAlg | oqsName | publicKeyBytes | privateKeyBytes | signatureBytes | status |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| ML-DSA-44 | -48 | ML-DSA-44 | 1312 | 2560 | 2420 | stable in repo |
| ML-DSA-65 | -49 | ML-DSA-65 | 1952 | 4032 | 3309 | stable in repo |
| ML-DSA-87 | -50 | ML-DSA-87 | 2592 | 4896 | 4627 | stable in repo |
| FN-DSA-512 | -54 | Falcon-512 | 897 | 1281 | 752 | planned |
| FN-DSA-1024 | -55 | Falcon-1024 | 1793 | 2305 | 1462 | planned |

說明：

1. `oqsName` 之所以還是 `Falcon-*`，是因為目前本機 `liboqs` 環境就是這樣命名。
2. FN-DSA 的 byte 長度應以實際 `liboqs` 版本為準，接入前請再檢查一次。

### 5.2 避免 mapping 分散失控

這個專案目前的 mapping 分散在多個地方，如果未來直接各改各的，很容易出現：

1. RP 宣告了 `-54/-55`
2. Authenticator 可以選到 `-54/-55`
3. 但 verifier 端沒有對應的 `oqs` 名稱
4. 或 extension 的 byte-size constants 沒同步更新

整合時一定要同時確認：

1. `COSE alg`
2. `oqs` 名稱
3. key / signature byte-size

這三者必須一起更新。

## 6. FN-DSA 整合 SOP

新增 `FN-DSA` 時，請依照以下順序處理。

### Step 1. 先固定演算法編號

本專案後續整合統一使用：

1. `FN-DSA-512` -> `-54`
2. `FN-DSA-1024` -> `-55`

這一步必須先定下來，後面的 RP、Authenticator、DB、測試都會依賴這組值。

### Step 2. 更新 RP Server 的演算法宣告

目標是讓 RP 能在註冊 options 中宣告 `FN-DSA`。

需要處理的點：

1. `rp_server/config.py`
   把 `-54`、`-55` 放進 `hosted_algorithms`
2. `rp_server/app.py`
   確認 `pubKeyCredParams` 會把新 `alg` 帶出去
3. `rp_server/services.py`
   - `verify_registration_payload()` 允許新的 `alg`
   - `COSE_TO_OQS` 補上 `-54/-55`
   - `_cose_to_oqs()` 能回傳正確的 verifier 名稱

注意：

1. RP 是整個流程的協定入口，若 RP 沒宣告 `FN-DSA`，Authenticator 就不應該私自選它。
2. RP 驗證時使用的 `oqs` 名稱，必須與 Authenticator 產生簽章時使用的名稱完全一致。

### Step 3. 更新 Python authenticator 的簽章映射

若沿用 README 目前啟動的 Python authenticator 路線，需要修改：

1. `authenticator/pqcrypto.py`
   - 新增 `-54 -> Falcon-512`
   - 新增 `-55 -> Falcon-1024`
   - 確認 `PQCSignatureSuite` 可接受新的 `alg`
2. `authenticator/webauthn.py`
   - 原則上不用改結構
   - 只要確認 `build_credential_public_key()` 的 `algorithm` 可帶入 `-54/-55`

重點：

1. 這個 repo 目前的 `credentialPublicKey` 是 `AKP + alg + -1=pubkey`
2. `FN-DSA` 若沿用同一種表示法，改的是 mapping，不是整個 WebAuthn binary 結構

### Step 4. 若維護 extension 版 authenticator，也要同步修改

若未來主線改成 extension 版，則要同步更新：

1. `extension/src/types/messages.ts`
   `SupportedAlg` 型別加上 `-54/-55`
2. `extension/src/background/authenticator.ts`
   - `SUPPORTED_ALGORITHMS`
   - `toSupportedAlg()`
   - `selectAlgorithm()`
   - `credentialPublicKeyCose()`
3. `extension/src/background/pq-signer.ts`
   補上 `FN-DSA` 的 key / signature 長度
4. `extension/wasm/pq_bridge.c`
   `pq_alg_name()` 補上 `-54/-55` 對應的 `Falcon-*`

這裡最常漏掉的是：

1. 型別有加，但 byte-size constants 沒加
2. TS 層有加，但 C / wasm bridge 沒加
3. 註冊能過，但 assertion 在 sign 時才爆掉

### Step 5. 補齊測試案例

`FN-DSA` 接入後，至少要有以下測試：

1. RP `pubKeyCredParams` 包含 `-54/-55`
2. Authenticator 能在 request order 中選到 `FN-DSA`
3. 註冊產出的 `attestationObject` 中，`credentialPublicKey[3]` 是 `-54` 或 `-55`
4. 註冊後 DB / storage 會正確存下 `FN-DSA` 的 `algorithm`
5. assertion 可以用對應公鑰驗章成功
6. 如果 RP 沒宣告 `FN-DSA`，Authenticator 不能私自選 `FN-DSA`

### Step 6. 做一次端到端驗證

端到端檢查順序如下：

1. 啟 RP Server
2. 啟 frontend
3. 啟 authenticator
4. 讓 RP `pubKeyCredParams` 只留下 `-54` 或 `-55`
5. 完整走一遍 register
6. 完整走一遍 authenticate
7. 檢查 DB / storage 中 `algorithm` 是否和預期一致

## 7. 交接口語

以下內容可直接作為口頭交接稿：

> 這個專案把 PQ 演算法整合進 WebAuthn 的方式，重點不是改瀏覽器標準，而是讓 RP、Authenticator、Verifier 三邊對同一個 COSE `alg` 有一致解讀。  
> 目前 repo 正式支援的是 ML-DSA `-48/-49/-50`。  
> 如果接下來要新增 FN-DSA，就統一使用 `FN-DSA-512 -> -54`、`FN-DSA-1024 -> -55`。  
> 實作上雖然 `liboqs` 仍可能使用 `Falcon-512`、`Falcon-1024` 這些名稱，但對專案文件、流程與測試來說，我們一律用 `FN-DSA` 來描述。

## 8. 實作順序

開始新增 `FN-DSA` 時，建議依照以下順序處理：

1. 先補 shared algorithm registry
2. 先讓 RP + Python authenticator 跑通註冊與驗證
3. 再決定 extension 版是否也要同步支援
4. 最後補完整測試

原因如下：

1. 先把 mapping 固定，後面才不會重工
2. 先通 RP + authenticator 主流程，才能確認協定面沒有誤解
3. extension/wasm 是額外維護成本，適合在核心流程穩定後再做

## 9. 參考資料

1. IANA COSE Algorithms registry
   https://www.iana.org/assignments/cose/cose.xhtml
2. IETF draft: COSE support for FN-DSA
   https://datatracker.ietf.org/doc/draft-ietf-cose-falcon/
