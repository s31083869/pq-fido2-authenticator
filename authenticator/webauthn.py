"""Utilities for constructing WebAuthn-compliant binary structures."""

from __future__ import annotations

import hashlib
from typing import Optional

from fido2 import cbor

from .models import CredentialRecord, b64url_decode

FLAG_UP = 0x01
FLAG_UV = 0x04
FLAG_AT = 0x40
AAGUID = bytes(16)


def build_credential_public_key(record: CredentialRecord, algorithm: int) -> bytes:
    """Encode the PQ public key as a COSE_Key structure."""
    public_key_bytes = b64url_decode(record.public_key)
    cose_key = {
        1: 7,  # AKP key type, matching the working Chrome extension payload
        3: algorithm,
        -1: public_key_bytes,
    }
    return cbor.encode(cose_key)


def build_authenticator_data(
    rp_id: str,
    sign_count: int,
    credential_id: Optional[bytes] = None,
    credential_public_key: Optional[bytes] = None,
    user_verified: bool = True,
) -> bytes:
    rp_hash = hashlib.sha256(rp_id.encode("idna")).digest()
    flags = FLAG_UP
    if user_verified:
        flags |= FLAG_UV
    include_attestation = credential_id is not None and credential_public_key is not None
    if include_attestation:
        flags |= FLAG_AT

    data = bytearray()
    data.extend(rp_hash)
    data.append(flags)
    data.extend(sign_count.to_bytes(4, "big"))

    if include_attestation:
        data.extend(AAGUID)
        data.extend(len(credential_id).to_bytes(2, "big"))
        data.extend(credential_id)
        data.extend(credential_public_key)

    return bytes(data)


def build_attestation_object(auth_data: bytes) -> bytes:
    return cbor.encode({"fmt": "none", "authData": auth_data, "attStmt": {}})
