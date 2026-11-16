# 專案守則

這份文件是本專案的協作守則，Claude 每次開新對話都會讀取並遵守，人也可以直接閱讀。內容於 2026-11-16 與使用者逐項確認，修改前要先取得使用者同意。

## 專案文件

| 文件 | 用途 |
|---|---|
| `codex/PROTOCOL-GUIDE.html` | 協議導覽：從零理解本專案，內含名詞表（第 11 章）。用瀏覽器開啟 |
| `workflow.md` | FN-DSA 整合的功能表（F01–F19） |
| `codex/FN-DSA-PLAN.md` | FN-DSA 每日實作計畫 |
| `codex/worklog/day-NN.md` | 每個 Day 的工作紀錄 |
| `codex/REPORTS.md` | 決策紀錄（Decision Log） |
| `codex/docs/FALCON_INTEGRATION_HANDOVER.md` | FN-DSA 交接文件 |

## 語言與註解

- 變數、函式、類別等名稱用英文。
- 註解、文件、commit 訊息、PR 說明一律用繁體中文。
- 所有新寫或修改的程式（包含測試）都要有精準的繁體中文註解：
  - 每個函式與類別說明「做什麼、為什麼、輸入與輸出」。
  - 每個有意義的區塊說明它在 WebAuthn 或密碼學上的意義，例如「authData 第 33–36 bytes 是 signCount，大端序」。
  - 不寫只是重講語法的註解（例如「i 加 1」）。
- 不回頭替整份既有檔案補註解；但只要修改到某個函式，就把整個函式的註解補齊。

## 協作方式

- 由 Claude 寫程式，使用者審閱 diff 並提問。
- 每個任務開始前，Claude 先說明「要改哪裡、為什麼、跟整體架構的關係」。
- 開始實作前，雙方必須確認理解一致（見「每日流程」第 3 步）。

## 每日流程

分支對應的是 `codex/FN-DSA-PLAN.md` 裡的 Day，不是日曆日期。

1. **準備**：`git fetch`，確認前一個 Day 已合併進 `main`，再從 `origin/main` 開出 `day-NN` 分支（例如 `day-02`）。
2. **寫開工文件**：在 `codex/worklog/day-NN.md` 寫好開工段落：今日目標、架構背景、預計修改、測試案例（情境 → 預期結果 → 依據）。
3. **介紹與對齊**：
   1. Claude 介紹今天的內容。
   2. 使用者回答理解之後，Claude 再問 2–3 個確認問題。
   3. 理解有落差就補充說明，直到對上為止。
   4. 使用者核准測試案例。問答與核准結果記進開工段落。
4. **先 commit 開工文件**（`Day N: 開工文件與測試案例`），證明測試案例在實作之前就定好了。
5. **逐項實作**：每完成一項就 commit 一次，訊息格式為 `Day N: 這一項做了什麼`。
6. **收尾**：補完工段落（每處修改列出 `檔案:行號範圍 → 改了什麼 → 目的`，附 commit）、更新計畫勾選、交給獨立子代理審查，最後 commit `Day N: 完工紀錄`。
7. **交付**：push 分支，Claude 用 `gh` 開 PR（說明放摘要與工作紀錄連結），CI 跑完後由使用者審閱並合併。

當天沒做完：隔天在同一個分支繼續，該 Day 的任務全部完成才開 PR，計畫日期整體順延。

## Git 規則

- 合併到 `main` 由使用者在 GitHub 上操作。Claude 不可以直接 push 或合併到 `main`。
- commit 只加入這次任務相關的檔案，不使用 `git add -A`。
- 不可以跳過 hook，也不可以改寫已經 push 的歷史。

## 範圍與禁止事項

- 只改當天任務需要的地方。中途發現的其他問題，記到工作紀錄的待辦清單，不當場修。
- 不修改第三方或自動產生的資料夾：`extension/emsdk`、`extension/.deps`、`.venv`、`node_modules`、`dist`。
- 不動使用者的資料檔：`rp_server/data/`、`authenticator/data/`。
- 新增或升級任何依賴套件（包括 liboqs）之前，要先問使用者。

## 測試要求

### TDD

- 改到程式邏輯時（設定與文件除外），先寫一個會失敗的測試，確認它真的失敗後再實作。
- 修 bug 時，先寫一個能重現 bug 的測試。

### 避免球員兼裁判

1. 測試案例由使用者核准（開工文件中的「情境 → 預期結果 → 依據」）。
2. 預期值必須來自外部依據：`workflow.md` 的驗收標準、規格書、RFC、官方 KAT。禁止先跑程式、再把輸出抄進測試。
3. 實作前跑出的紅燈結果要記進工作紀錄。失敗的測試不 commit。
4. 關鍵測試要做破壞檢查：故意把實作改壞一次，確認測試會失敗，再改回來。
5. 開 PR 前，交給一個沒看過實作過程的子代理，對照核准的測試案例審查測試與 diff，結果記進工作紀錄。
6. 已核准的測試不能被改弱：要改預期值、刪除或跳過測試，都必須先經過使用者同意。

### 每次 commit 前必須全部通過

```bash
uv run pytest
uv run ruff check authenticator rp_server
uv run ruff format --check authenticator rp_server
cd extension && bun test src && bun run typecheck
cd frontend && bun test src && bun run lint && bunx tsc --noEmit
```

新增 `tests/` 資料夾後，要同步加進 `pyproject.toml` 的 `testpaths` 與上面的 ruff 路徑。

### 其他要求

- **真實密碼學**：單元測試可以用假的簽章器測流程，但共用演算法表裡的每個演算法，都至少要有一個用真的 liboqs 跑「產生金鑰 → 簽章 → RP 驗章」的測試。
- **KAT**：官方 KAT 測試做好之後，納入上面的必跑清單。liboqs 的任何變動（升級、重建 WASM、改編譯清單）都必須通過。
- **測試位置**：單一元件的單元測試放在 `authenticator/tests/`、`rp_server/tests/`、`extension/src/**/*.test.ts`；跨元件的整合測試放 `tests/integration/`；KAT 測試放 `tests/kat/`。
- **命名**：測試函式用英文描述行為（例如 `test_selects_fn_dsa_when_rp_offers_it`），註解用繁體中文說明測什麼、依據哪條需求。
- **端到端測試**：Python 路線完成時、Extension 路線完成時、最後回歸時各一次。由使用者照 Claude 準備的清單親手執行，使用真的 Windows Hello，結果記進工作紀錄。
- **CI**：GitHub Actions 在 `ubuntu-latest` 上跑必跑清單，PR 建立或更新時觸發。看到紅叉就不合併。
- **pyright**：暫不納入。

## 文件維護

- 每個 Day 一份 `codex/worklog/day-NN.md`，分成開工與完工兩段，跟程式一起 commit。
- 新術語第一次出現時，加進 `codex/PROTOCOL-GUIDE.html` 第 11 章的名詞表。這是唯一的名詞表。
- 程式或流程有變動，影響到協議導覽的內容時，一併更新導覽。
- 重大決策記到 `codex/REPORTS.md` 的 Decision Log。

## 環境注意事項

- liboqs 原生函式庫裝在 `C:\Users\user\_oqs`（0.14.0）。若找不到，第一次 `import oqs` 時會自動從網路下載並編譯 liboqs；需要時先問使用者，不要在不知情的情況下觸發。
- Extension 的 WASM 由 `extension/scripts/` 的腳本在 Git Bash 中建置，需要 `extension/emsdk`、CMake 與 `C:\mingw64` 的 mingw32-make。
- Python authenticator 在 Windows 上會跳出 Windows Hello；自動化測試一律使用 `NoopVerifier`。
