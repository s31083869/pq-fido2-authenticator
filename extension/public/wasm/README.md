# `public/wasm/`

Generated wasm output directory.

## Artifact

1. `pq_bridge.wasm`

## How to Generate

```bash
bun run setup:liboqs:wasm
bun run build:wasm
```

## Runtime Use

1. loaded via `chrome.runtime.getURL("wasm/pq_bridge.wasm")`
2. consumed by background service worker only
