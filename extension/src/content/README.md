# `src/content/`

Content script bridge layer.

## Responsibilities

1. inject `injected.js` into page main-world
2. forward hook requests to background (`chrome.runtime.sendMessage`)
3. return normalized responses/errors to page via `window.postMessage`
4. respect extension settings (`enabled`) before installing hook bridge

## Why this layer exists

1. `navigator.credentials` can only be patched safely in main-world
2. extension privileged APIs (`chrome.runtime`) are only available in extension worlds
3. content script provides the required trust boundary crossing
