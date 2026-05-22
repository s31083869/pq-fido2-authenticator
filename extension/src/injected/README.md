# `src/injected/`

Main-world WebAuthn hook implementation.

## Responsibilities

1. monkey-patch:
   1. `navigator.credentials.create`
   2. `navigator.credentials.get`
2. serialize browser-native option objects into extension bridge payloads
3. rebuild `PublicKeyCredential`-like objects from extension responses
4. preserve fallback to original API when no `publicKey` options are provided

## Message Contract

1. request source tag: `PQ_WEBAUTHN_INJECTED`
2. response source tag: `PQ_WEBAUTHN_CONTENT`
3. per-request correlation id via `requestId`
