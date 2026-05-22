# 007 - CSP / Web Accessible Resource Surface Minimization

## Severity

`Low`

## Summary

目前 CSP 與 `web_accessible_resources` 配置偏寬，對於最小權限原則仍有收斂空間。

## Affected Code

1. `extension/public/manifest.json:13`
2. `extension/public/manifest.json:24`

## Why It Matters

1. `wasm-unsafe-eval` 在 MV3 wasm 場景可理解，但仍需嚴格控制其作用範圍。
2. `chunks/*`、`assets/*` 全開會增加可被探測與濫用的資源面。

## Recommended Fix

1. 只暴露必要檔案（明確列名，避免萬用字元）。
2. 若可行，將 injected 依賴打包成固定單檔以縮小暴露集合。
3. 針對 manifest 權限與資源清單做定期審查。

## Verification Checklist

1. 移除不必要的 `web_accessible_resources` 後功能仍正常。
2. extension 能載入 wasm，但資源暴露面較目前更小。

## Learning Note

CSP 和資源白名單是「減攻擊面」工具；功能可用不是終點，權限最小化才是長期穩定策略。
