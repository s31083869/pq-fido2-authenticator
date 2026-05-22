## Methods

### WebAuthn.addCredential
**Description:** Adds the credential to the specified authenticator.  
**Parameters:**
- `authenticatorId` — *AuthenticatorId*
- `credential` — *Credential*

---

### WebAuthn.addVirtualAuthenticator
**Description:** Creates and adds a virtual authenticator.  
**Parameters:**
- `options` — *VirtualAuthenticatorOptions*

**Return:**
- `authenticatorId` — *AuthenticatorId*

---

### WebAuthn.clearCredentials
**Description:** Clears all the credentials from the specified device.  
**Parameters:**
- `authenticatorId` — *AuthenticatorId*

---

### WebAuthn.disable
**Description:** Disable the WebAuthn domain.

---

### WebAuthn.enable
**Description:** Enable the WebAuthn domain and start intercepting credential storage and retrieval with a virtual authenticator.  
**Parameters:**
- `enableUI` — *boolean*  
  Whether to enable the WebAuthn user interface. Enabling the UI is recommended for debugging and demo purposes, as it is closer to the real experience. Disabling the UI is recommended for automated testing. Supported at the embedder's discretion if UI is available. Defaults to `false`.

---

### WebAuthn.getCredential
**Description:** Returns a single credential stored in the given virtual authenticator that matches the credential ID.  
**Parameters:**
- `authenticatorId` — *AuthenticatorId*
- `credentialId` — *string*

**Return:**
- `credential` — *Credential*

---

### WebAuthn.getCredentials
**Description:** Returns all the credentials stored in the given virtual authenticator.  
**Parameters:**
- `authenticatorId` — *AuthenticatorId*

**Return:**
- `credentials` — *array[Credential]*

---

### WebAuthn.removeCredential
**Description:** Removes a credential from the authenticator.  
**Parameters:**
- `authenticatorId` — *AuthenticatorId*
- `credentialId` — *string*

---

### WebAuthn.removeVirtualAuthenticator
**Description:** Removes the given authenticator.  
**Parameters:**
- `authenticatorId` — *AuthenticatorId*

---

### WebAuthn.setAutomaticPresenceSimulation
**Description:** Sets whether tests of user presence will succeed immediately (if `true`) or fail to resolve (if `false`). Default `true`.  
**Parameters:**
- `authenticatorId` — *AuthenticatorId*
- `enabled` — *boolean*

---

### WebAuthn.setCredentialProperties
**Description:** Allows setting credential properties.  
Spec: https://w3c.github.io/webauthn/#sctn-automation-set-credential-properties  
**Parameters:**
- `authenticatorId` — *AuthenticatorId*
- `credentialId` — *string*
- `backupEligibility` — *boolean*
- `backupState` — *boolean*

---

### WebAuthn.setResponseOverrideBits
**Description:** Resets parameters `isBogusSignature`, `isBadUV`, `isBadUP` to `false` if not present.  
**Parameters:**
- `authenticatorId` — *AuthenticatorId*
- `isBogusSignature` — *boolean*  
  If set, overrides the signature in the authenticator response to be zero. Defaults `false`.
- `isBadUV` — *boolean*  
  If set, overrides the UV bit in the flags in the authenticator response to be zero. Defaults `false`.
- `isBadUP` — *boolean*  
  If set, overrides the UP bit in the flags in the authenticator response to be zero. Defaults `false`.

---

### WebAuthn.setUserVerified
**Description:** Sets whether **User Verification** succeeds or fails for an authenticator. Default `true`.  
**Parameters:**
- `authenticatorId` — *AuthenticatorId*
- `isUserVerified` — *boolean*

---

## Events

### WebAuthn.credentialAdded
**Triggered when** a credential is added to an authenticator.  
**Parameters:**
- `authenticatorId` — *AuthenticatorId*
- `credential` — *Credential*

---

### WebAuthn.credentialAsserted
**Triggered when** a credential is used in a WebAuthn assertion.  
**Parameters:**
- `authenticatorId` — *AuthenticatorId*
- `credential` — *Credential*

---

### WebAuthn.credentialDeleted
**Triggered when** a credential is deleted (e.g., via `PublicKeyCredential.signalUnknownCredential()`).  
**Parameters:**
- `authenticatorId` — *AuthenticatorId*
- `credentialId` — *string*

---

### WebAuthn.credentialUpdated
**Triggered when** a credential is updated (e.g., via `PublicKeyCredential.signalCurrentUserDetails()`).  
**Parameters:**
- `authenticatorId` — *AuthenticatorId*
- `credential` — *Credential*

---

## Types

### WebAuthn.AuthenticatorId
- **Type:** `string`

---

### WebAuthn.AuthenticatorProtocol
- **Type:** `string`  
- **Allowed Values:** `u2f`, `ctap2`

---

### WebAuthn.AuthenticatorTransport
- **Type:** `string`  
- **Allowed Values:** `usb`, `nfc`, `ble`, `cable`, `internal`

---

### WebAuthn.Credential
- **Type:** `object`  
- **Properties:**
  - `credentialId` — *string*
  - `isResidentCredential` — *boolean*
  - `rpId` — *string*  
    Relying Party ID the credential is scoped to. Must be set when adding a credential.
  - `privateKey` — *string*  
    The **ECDSA P-256** private key in **PKCS#8** format. *(Encoded as base64 when passed over JSON)*
  - `userHandle` — *string*  
    Opaque byte sequence (max 64 bytes) mapping the credential to a specific user. *(base64 over JSON)*
  - `signCount` — *integer*  
    Signature counter; incremented per successful assertion. See https://w3c.github.io/webauthn/#signature-counter
  - `largeBlob` — *string*  
    Associated large blob. See https://w3c.github.io/webauthn/#sctn-large-blob-extension *(base64 over JSON)*
  - `backupEligibility` — *boolean*  
    Assertions will have **BE** flag set to this value. Defaults to authenticator’s `defaultBackupEligibility`.
  - `backupState` — *boolean*  
    Assertions will have **BS** flag set to this value. Defaults to authenticator’s `defaultBackupState`.
  - `userName` — *string*  
    Maps to `user.name`. Empty if not set. https://w3c.github.io/webauthn/#dom-publickeycredentialentity-name
  - `userDisplayName` — *string*  
    Maps to `user.displayName`. Empty if not set. https://w3c.github.io/webauthn/#dom-publickeycredentialuserentity-displayname

---

### WebAuthn.Ctap2Version
- **Type:** `string`  
- **Allowed Values:** `ctap2_0`, `ctap2_1`

---

### WebAuthn.VirtualAuthenticatorOptions
- **Type:** `object`  
- **Properties:**
  - `protocol` — *AuthenticatorProtocol*
  - `ctap2Version` — *Ctap2Version*  
    Defaults to `ctap2_0`. **Ignored if** `protocol == u2f`.
  - `transport` — *AuthenticatorTransport*
  - `hasResidentKey` — *boolean* (default `false`)
  - `hasUserVerification` — *boolean* (default `false`)
  - `hasLargeBlob` — *boolean*  
    If `true`, supports **largeBlob** extension. https://w3c.github.io/webauthn#largeBlob (default `false`)
  - `hasCredBlob` — *boolean*  
    If `true`, supports **credBlob** extension.  
    https://fidoalliance.org/specs/fido-v2.1-rd-20201208/fido-client-to-authenticator-protocol-v2.1-rd-20201208.html#sctn-credBlob-extension (default `false`)
  - `hasMinPinLength` — *boolean*  
    If `true`, supports **minPinLength** extension.  
    https://fidoalliance.org/specs/fido-v2.1-ps-20210615/fido-client-to-authenticator-protocol-v2.1-ps-20210615.html#sctn-minpinlength-extension (default `false`)
  - `hasPrf` — *boolean*  
    If `true`, supports **prf** extension. https://w3c.github.io/webauthn/#prf-extension (default `false`)
  - `automaticPresenceSimulation` — *boolean*  
    If `true`, tests of user presence succeed immediately. (default `true`)
  - `isUserVerified` — *boolean*  
    Sets whether **User Verification** succeeds or fails. (defaults to `false`)
  - `defaultBackupEligibility` — *boolean*  
    Credentials created will have **BE** flag set to this value. (default `false`)  
    https://w3c.github.io/webauthn/#sctn-credential-backup
  - `defaultBackupState` — *boolean*  
    Credentials created will have **BS** flag set to this value. (default `false`)  
    https://w3c.github.io/webauthn/#sctn-credential-backup
