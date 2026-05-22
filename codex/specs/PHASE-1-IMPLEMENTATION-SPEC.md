# PQ WebAuthn Extension Phase-1 Implementation Spec

Version: `v0.3-draft`  
Date: `2026-02-08`  
Status: `Implementation baseline + security backlog tracked`  
Owner: `codex + scalebear`

## 1. Scope

This document freezes the implementation behavior for:

1. M1 Registration (`navigator.credentials.create` hook path)
2. M2 Assertion (`navigator.credentials.get` hook path)

Target RP for validation:

1. `https://demo.yubico.com/webauthn-developers`

Out of scope for this freeze:

1. Cross-browser support beyond Chrome
2. Fallback to classical algorithms
3. Production-grade strong UV integration details

## 2. Fixed Constraints

1. `PQ-only` mode
2. Supported COSE algorithms: `-48`, `-49`, `-50`
3. Default algorithm preference: `-48` (ML-DSA-44)
4. Attestation mode: `none`
5. Hook enablement scope: `demo.yubico.com` only (v1)
6. Runtime signer path: `wasm-only` (`liboqs C + Emscripten wasm`)

Attestation negotiation rule (v0.1):

1. RP may request `attestation: "direct"` (observed on Yubico demo).
2. Extension trial implementation still returns `attestationObject.fmt = "none"`.
3. This is allowed as authenticator behavior in this phase; we do not emit attestation certificates in v0.1.

Algorithm mapping:

1. `-48 -> ML-DSA-44`
2. `-49 -> ML-DSA-65`
3. `-50 -> ML-DSA-87`

## 3. Encoding and Canonical Rules

1. Binary fields in JSON transport MUST use base64url without padding.
2. Incoming base64url fields MUST be decoded before cryptographic operations.
3. `clientDataJSON` MUST be UTF-8 JSON bytes.
4. `rpIdHash` MUST be `SHA-256(rpId)` using IDNA-normalized `rpId`.
5. Signature input for assertion MUST be:

```text
authenticatorData || SHA-256(clientDataJSON)
```

Compatibility input normalization (trial phase):

1. For incoming binary-like fields (`challenge`, `user.id`, credential descriptor `id`), extension MAY accept:
   1. base64url (preferred)
   2. base64
   3. lowercase/uppercase hex string
2. Internal canonical representation MUST be bytes.
3. Hook boundary output SHOULD remain base64url for web-facing JSON shapes.

## 4. Data Model Freeze

### 4.1 Credential Descriptor vs Credential Public Key

1. WebAuthn descriptor remains:

```json
{ "type": "public-key", "id": "<credentialId>" }
```

2. `credentialPublicKey` in `authData` uses COSE_Key.

### 4.2 credentialPublicKey (COSE_Key)

Current freeze baseline:

1. `1` (kty) = `7` (AKP)
2. `3` (alg) = selected `-48/-49/-50`
3. `-1` = raw ML-DSA public key bytes

Note:

1. Legacy custom marker field `-70001` is removed.
2. RP-side verification must recognize AKP + `alg -48/-49/-50`.

### 4.3 authenticatorData Flags and signCount

Flag bits:

1. `UP = 0x01`
2. `UV = 0x04`
3. `AT = 0x40`

Frozen values:

1. Registration (`create`): `UP + UV + AT = 0x45`
2. Assertion (`get`): `UP + UV = 0x05`

signCount behavior:

1. Initial value at registration: `0`
2. On successful assertion: increment by `1`
3. First successful assertion returns `1`

## 5. M1 Registration Flow Freeze

### 5.0 Observed RP Baseline (Yubico Demo)

Observed `PublicKeyCredentialCreationOptions` characteristics from `demo.yubico.com`:

1. `attestation: "direct"`
2. `authenticatorSelection.userVerification: "preferred"`
3. `extensions.credProps: true`
4. `pubKeyCredParams` includes `-48/-49/-50`
5. `rp.id = "demo.yubico.com"`
6. `timeout = 90000`

Frozen handling for this baseline:

1. Accept incoming `attestation` value but emit `fmt=none` in response.
2. Accept `credProps` input; extension may return empty/limited extension results in trial phase.
3. Keep algorithm selection rule unchanged (first supported alg by request order).

### 5.0.1 Observed Legacy Bridge Sample (Playwright + custom authenticator)

Observed facts from provided sample:

1. Input `challenge` and `user.id` appeared as hex strings.
2. RP requested `attestation: "direct"`, while returned attestation format was `none`.
3. Parsed authenticator flags were `69` (`0x45` = `UP+UV+AT`).
4. Parsed signature counter at registration was `0`.
5. `publicKeyAlgorithm` in response was `-48`.
6. AAGUID was all-zero (`00000000000000000000000000000000`).
7. `clientDataJSON` did not include `crossOrigin` key.

Freeze implications:

1. Keep accepting `attestation: "direct"` while returning `fmt=none`.
2. Add input decoding compatibility for hex challenge/user IDs.
3. Treat missing `crossOrigin` as equivalent to `false` in trial validation.

## 5.1 Input Requirements

Required request fields:

1. `publicKey.rp.id`
2. `publicKey.user.id`
3. `publicKey.challenge`
4. `publicKey.pubKeyCredParams`

Optional but supported:

1. `excludeCredentials`
2. `timeout`
3. `authenticatorSelection`
4. `attestation`
5. `extensions`

## 5.2 Algorithm Selection

1. Iterate `pubKeyCredParams` in request order.
2. Select the first algorithm in `{-48,-49,-50}`.
3. If none found, throw `NotSupportedError`.

## 5.3 excludeCredentials Rule

1. Compare incoming `excludeCredentials[].id` with stored credential IDs for same `rpId`.
2. If any match, abort with `InvalidStateError`.

## 5.4 UV Gate

1. `create` response must only continue after UV success.
2. In trial phase, UV provider may be software UV.
3. Strong OS UV is a separate integration layer and does not change payload format in this spec.

## 5.5 Registration Payload Build

1. Generate credential keypair using selected ML-DSA parameter set.
2. Generate random credential ID (`32` bytes baseline).
3. Build `clientDataJSON`:

```json
{
  "type": "webauthn.create",
  "challenge": "<base64url challenge>",
  "origin": "<page origin>"
}
```

Note:

1. Trial implementation includes `crossOrigin: false` in `clientDataJSON`.

4. Build `credentialPublicKey` as frozen in section 4.2.
5. Build `authenticatorData`:
   1. `rpIdHash`
   2. flags `0x45`
   3. signCount `0`
   4. attestedCredentialData (`AAGUID(16x00)`, credentialId length, credentialId, credentialPublicKey)
6. Build `attestationObject`:

```cbor
{
  "fmt": "none",
  "authData": <authenticatorData bytes>,
  "attStmt": {}
}
```

## 5.6 create() Return Shape

1. Top-level:
   1. `id`
   2. `rawId`
   3. `type = "public-key"`
2. `response`:
   1. `clientDataJSON`
   2. `attestationObject`
   3. optional helper fields allowed in local implementation (`publicKey`, `publicKeyAlgorithm`, `authenticatorData`)

## 6. M2 Assertion Flow Freeze

## 6.1 Input Requirements

Required:

1. `publicKey.challenge`

Optional:

1. `publicKey.rpId`
2. `publicKey.allowCredentials`
3. `publicKey.userVerification`
4. `publicKey.timeout`
5. `publicKey.extensions`

## 6.2 allowCredentials Rule

1. If `allowCredentials` present and non-empty:
   1. Select first stored credential whose ID is in allow-list and `rpId` matches.
   2. If none found, abort with `NotAllowedError`.
2. If `allowCredentials` absent/empty:
   1. Select first stored credential by `rpId`.
   2. If none found, abort with `NotAllowedError`.

## 6.3 UV Gate

1. `get` response must only continue after UV success.
2. UV level does not alter flags in this freeze (`0x05` is fixed for success path).

## 6.4 Assertion Payload Build

1. Build `clientDataJSON`:

```json
{
  "type": "webauthn.get",
  "challenge": "<base64url challenge>",
  "origin": "<page origin>"
}
```

Note:

1. Trial implementation includes `crossOrigin: false` in `clientDataJSON`.

2. Compute `clientDataHash = SHA-256(clientDataJSON)`.
3. Compute `newSignCount = storedSignCount + 1`.
4. Build `authenticatorData`:
   1. `rpIdHash`
   2. flags `0x05`
   3. signCount `newSignCount`
5. Compute signature over:

```text
authenticatorData || clientDataHash
```

6. Persist `newSignCount` only after successful signature generation.

## 6.5 get() Return Shape

1. Top-level:
   1. `id`
   2. `rawId`
   3. `type = "public-key"`
2. `response`:
   1. `clientDataJSON`
   2. `authenticatorData`
   3. `signature`
   4. `userHandle` (nullable)

## 7. Error Contract (Extension Side)

Implementation should normalize internal failures to WebAuthn-like errors:

1. No supported alg from `pubKeyCredParams` -> `NotSupportedError`
2. Credential already exists in `excludeCredentials` -> `InvalidStateError`
3. No available credential for assertion -> `NotAllowedError`
4. UV failed/cancelled/timeout -> `NotAllowedError`
5. Data validation failed (missing required field) -> `TypeError` or `DataError`

## 8. Trial-and-Error Test Matrix

M1 tests:

1. create success with `pubKeyCredParams=[-48]`
2. create success with ordered params `[-7,-49]` (must choose `-49`)
3. create failure with params excluding `-48/-49/-50`
4. create failure when `excludeCredentials` includes existing credential ID
5. create payload contains `fmt=none` and flags `0x45`
6. create accepts hex-encoded `challenge` and `user.id` inputs

M2 tests:

1. get success with explicit `allowCredentials` match
2. get success without `allowCredentials` (rpId-based default selection)
3. get failure with unmatched allow-list
4. first successful get returns signCount `1`
5. second successful get returns signCount `2`
6. signature verifies over `authData || hash(clientDataJSON)`

Compatibility tests against Yubico demo:

1. Register flow end-to-end on demo page
2. Authenticate flow end-to-end on demo page
3. Repeat authenticate and confirm signCount monotonic behavior
4. Registration should still pass when RP requests `attestation: "direct"` and extension returns `fmt=none`

## 9. Open Items (Not Blocking M1/M2 Trial)

1. Strong UV provider implementation route:
   1. Pure extension software UV
   2. Native Messaging Host for OS-level UV
2. Storage encryption policy and key wrapping model

## 10. Exit Criteria for M1/M2 Freeze

M1 exit:

1. All M1 tests in section 8 pass
2. Demo registration succeeds with `attestation=none`
3. Stored credential material and metadata are retrievable by `rpId`

M2 exit:

1. All M2 tests in section 8 pass
2. Demo authentication succeeds
3. signCount is persisted and increments monotonically

## 11. Implementation Technology Baseline

1. Extension runtime: Chrome MV3 service worker + content script + injected main-world hook
2. PQ crypto path: `liboqs` C library compiled by Emscripten to `pq_bridge.wasm`
3. Supported algorithms in runtime: `ML-DSA-44/65/87` only
4. `liboqs` build strategy: minimal build (`SIG_ml_dsa_44;SIG_ml_dsa_65;SIG_ml_dsa_87`)
5. Transport encoding: JSON bridge + base64url for binary fields
6. Persistent storage: `chrome.storage.local` schema store (`pq_store_v1`)

## 12. Security Report Artifacts (UV Deferred)

1. `codex/SECURITY_REPORTS/README.md`
2. `codex/SECURITY_REPORTS/001-PLAIN_PRIVATE_KEY_STORAGE.md`
3. `codex/SECURITY_REPORTS/002-UNTRUSTED_PAGE_TRIGGER_NO_USER_GESTURE.md`
4. `codex/SECURITY_REPORTS/003-MISSING_RUNTIME_SCHEMA_VALIDATION.md`
5. `codex/SECURITY_REPORTS/004-SIGNCOUNT_RACE_CONDITION.md`
6. `codex/SECURITY_REPORTS/005-LIBOQS_UNPINNED_SOURCE_SUPPLY_CHAIN.md`
7. `codex/SECURITY_REPORTS/006-PRODUCTION_SOURCEMAP_EXPOSURE.md`
8. `codex/SECURITY_REPORTS/007-CSP_AND_RESOURCE_SURFACE_MINIMIZATION.md`

Policy note:

1. `UV` 相關安全議題依目前開發決策延後至最後階段，本輪不進入修補排程。

## 13. Spec Naming Migration

結論：`M1-M2-SPEC-FREEZE` 已不完全符合現況。

原因：

1. 內容已不只 M1/M2，而是涵蓋運行基線與安全追蹤。
2. 目前狀態也不再是純 freeze，而是持續演進中的 implementation spec。

遷移結果：

1. 新主檔：`codex/specs/PHASE-1-IMPLEMENTATION-SPEC.md`
2. 舊檔 `M1-M2-SPEC-FREEZE` 已移除，統一以本檔為唯一規格來源。
