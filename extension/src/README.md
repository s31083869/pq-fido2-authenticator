# `src/`

Application source tree for the extension.

## Directory Overview

1. `background/`
   1. service worker and authenticator runtime
2. `content/`
   1. page <-> extension relay
3. `injected/`
   1. WebAuthn API hook in main-world
4. `lib/`
   1. shared low-level utility modules
5. `options/`
   1. React settings page
6. `types/`
   1. shared contracts/models

## End-to-End Request Path

1. page calls `navigator.credentials.create/get`
2. injected hook serializes request
3. content script forwards to background
4. background runs authenticator and signer
5. response is reconstructed into credential-like object and returned to page
