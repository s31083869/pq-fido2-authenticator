from __future__ import annotations

import cbor2

from authenticator.models import CredentialRecord, b64url_encode
from authenticator.webauthn import (
    build_attestation_object,
    build_authenticator_data,
    build_credential_public_key,
)


def make_record() -> CredentialRecord:
    return CredentialRecord(
        credential_id="cred-id",
        user_handle="user",
        rp_id="example.com",
        algorithm=-49,
        public_key=b64url_encode(b"public"),
        private_key=b64url_encode(b"private"),
        sign_count=0,
    )


def test_build_credential_public_key_encodes_cose():
    record = make_record()
    encoded = build_credential_public_key(record, -49)
    decoded = cbor2.loads(encoded)
    assert decoded[1] == 7  # kty=AKP
    assert decoded[3] == -49  # alg
    assert decoded[-1] == b"public"


def test_build_authenticator_data_contains_attestation():
    auth_data = build_authenticator_data(
        rp_id="example.com",
        sign_count=5,
        credential_id=b"abc",
        credential_public_key=b"cose",
        user_verified=True,
    )
    assert len(auth_data) > 37
    # rpIdHash is first 32 bytes
    assert auth_data[:32] != b"\x00" * 32
    # Flags byte has UP + UV + AT bits set
    flags = auth_data[32]
    assert flags & 0x01
    assert flags & 0x04
    assert flags & 0x40
    # signCount stored next 4 bytes
    assert int.from_bytes(auth_data[33:37], "big") == 5


def test_build_attestation_object_wraps_data():
    auth_data = build_authenticator_data(
        rp_id="example.com",
        sign_count=0,
        credential_id=b"id",
        credential_public_key=b"key",
    )
    obj = build_attestation_object(auth_data)
    decoded = cbor2.loads(obj)
    assert decoded["fmt"] == "none"
    assert decoded["authData"] == auth_data
    assert decoded["attStmt"] == {}
