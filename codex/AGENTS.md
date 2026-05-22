## abstract

我要開發一個 chrome extension，當使用者在該網站啟用 extension 後，可以將原生的 navigator.credentials WebAuthn API 改為支援 Post-Quantum 的自定義 navigator.credentials WebAuthn API，使得瀏覽器支援 Post-Quantum 的 FIDO2 註冊驗證流程。

## Requirements

套件規範
- 使用 Vite + React + TypeScript + TailwindCSS 進行開發

## 核心概念

收到 WebAuthn Request 後，要求 User Verification (Touch ID / Windows Hello)，進行金鑰生成 (liboqs + wasm)，生成完畢之後，選擇安全的 storage API 進行儲存，並回傳 WebAuthn Response。

