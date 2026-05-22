# PQ FIDO2 Authenticator

## 快速開始

### 1. 安裝依賴

```bash
uv sync          # 安裝 Python 相依
cd frontend
bun install      # 安裝前端依賴
```

## 專案啟動 (請務必照順序)

### 2. 啟動 RP Server

```bash
uv run flask --app rp_server.app run --port 5005 --debug # Note: 在 project 根目錄運行
```

RP 預設使用 `sqlite:///rp_server/data/rp.db`，第一次啟動會自動建立資料庫。

### 3. 啟動前端

```bash
cd frontend
bun dev
```

### 4. 啟動 Authenticator

```bash
uv run python -m authenticator --url http://localhost:3000 # Note: 在 project 根目錄運行
```

### 5. 啟動 Database Studio (Optional)

```bash
cd drizzle
bun install      # 安裝依賴
bun run db:studio
```

使用瀏覽器到 https://local.drizzle.studio 就可以觀察 DB records 的變化啦

