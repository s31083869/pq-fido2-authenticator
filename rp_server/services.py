"""Business logic for RP server."""

from __future__ import annotations

import base64
import hashlib
import json
from io import BytesIO
import secrets
import string
from typing import List, Tuple

from flask import abort
import oqs
import cbor2
from sqlalchemy import select
from sqlalchemy.orm import Session

from .config import RPSettings
from .models import Credential, User


ALPHABET = string.ascii_letters + string.digits


def _generate_user_handle(length: int = 21) -> str:
    return "".join(secrets.choice(ALPHABET) for _ in range(length))


def new_user_handle(session: Session) -> str:
    handle = _generate_user_handle()
    while session.scalar(select(User).where(User.user_handle == handle)):
        handle = _generate_user_handle()
    return handle


def ensure_user(
    session: Session,
    username: str,
    display_name: str,
    user_handle: str | None = None,
) -> User:
    user = session.scalar(select(User).where(User.username == username))
    if user:
        if user.display_name != display_name:
            user.display_name = display_name
        return user
    user = User(
        username=username,
        display_name=display_name,
        user_handle=user_handle or new_user_handle(session),
    )
    session.add(user)
    session.flush()
    return user


def get_user(session: Session, username: str) -> User | None:
    return session.scalar(select(User).where(User.username == username))


def list_credentials(session: Session, user: User) -> List[Credential]:
    return list(session.scalars(select(Credential).where(Credential.user_id == user.id)))


def store_credential(
    session: Session,
    user: User,
    credential_id: str,
    public_key: str,
    algorithm: int,
) -> Credential:
    credential = Credential(
        id=credential_id,
        user_id=user.id,
        public_key=public_key,
        algorithm=algorithm,
        sign_count=0,
    )
    session.add(credential)
    session.flush()
    return credential


def verify_registration_payload(
    payload: dict,
    challenge: str,
    settings: RPSettings,
) -> Tuple[str, int, str]:
    response = payload.get("response", {})
    client_data_json = _b64url_to_bytes(response.get("clientDataJSON"))
    client_data = json.loads(client_data_json)
    if client_data.get("type") != "webauthn.create":
        abort(400, "Invalid clientData type")
    if client_data.get("challenge") != challenge:
        abort(400, "Challenge mismatch")
    if client_data.get("origin") != settings.origin:
        abort(400, "Origin mismatch")

    attestation_b64 = response.get("attestationObject")
    if not attestation_b64:
        abort(400, "Missing attestationObject")
    attestation = cbor2.loads(_b64url_to_bytes(attestation_b64))
    auth_data_bytes = attestation.get("authData")
    if not isinstance(auth_data_bytes, (bytes, bytearray)):
        abort(400, "Invalid authenticator data")
    parsed = _parse_authenticator_data(bytes(auth_data_bytes))
    if parsed.get("rp_id_hash") != _rp_id_hash(settings.rp_id):
        abort(400, "rpId hash mismatch")
    credential_id = parsed.get("credential_id")
    credential_public_key = parsed.get("credential_public_key")
    if credential_id is None or credential_public_key is None:
        abort(400, "Missing attested credential data")

    algorithm = credential_public_key.get(3)
    if algorithm not in settings.hosted_algorithms:
        abort(400, "Unsupported algorithm")

    public_key_bytes = credential_public_key.get(-1)
    if not isinstance(public_key_bytes, (bytes, bytearray)):
        abort(400, "Invalid public key")

    credential_id_b64 = _bytes_to_b64url(credential_id)
    public_key_b64 = _bytes_to_b64url(bytes(public_key_bytes))
    return credential_id_b64, algorithm, public_key_b64


def verify_authentication_payload(
    session: Session,
    payload: dict,
    challenge: str,
    settings: RPSettings,
    user: User,
) -> Credential:
    response = payload.get("response", {})
    credential_id = payload.get("id") or payload.get("rawId")
    credential = session.get(Credential, credential_id or "")
    if not credential or credential.user_id != user.id:
        abort(400, "Unknown credential")

    client_data = json.loads(_b64url_to_bytes(response.get("clientDataJSON")))
    if client_data.get("type") != "webauthn.get":
        abort(400, "Invalid clientData type")
    if client_data.get("challenge") != challenge:
        abort(400, "Challenge mismatch")
    if client_data.get("origin") != settings.origin:
        abort(400, "Origin mismatch")

    auth_data_bytes = _b64url_to_bytes(response.get("authenticatorData"))
    parsed = _parse_authenticator_data(auth_data_bytes)
    if parsed.get("rp_id_hash") != _rp_id_hash(settings.rp_id):
        abort(400, "rpId hash mismatch")

    message = auth_data_bytes + hashlib.sha256(
        json.dumps(client_data, separators=(",", ":")).encode("utf-8")
    ).digest()
    signature = _b64url_to_bytes(response.get("signature"))

    oqs_alg = _cose_to_oqs(credential.algorithm)
    with oqs.Signature(oqs_alg) as verifier:
        valid = verifier.verify(message, signature, _b64url_to_bytes(credential.public_key))
    if not valid:
        abort(400, "Invalid signature")

    credential.sign_count = parsed.get("sign_count", credential.sign_count)
    return credential


COSE_TO_OQS = {
    -48: "ML-DSA-44",
    -49: "ML-DSA-65",
    -50: "ML-DSA-87",
}


def _cose_to_oqs(alg: int) -> str:
    if alg not in COSE_TO_OQS:
        abort(400, "Unsupported algorithm")
    return COSE_TO_OQS[alg]


def _b64url_to_bytes(value: str | None) -> bytes:
    if not value:
        abort(400, "Missing base64 value")
    padding = "=" * (-len(value) % 4)
    return base64.urlsafe_b64decode(value + padding)


def _bytes_to_b64url(value: bytes) -> str:
    return base64.urlsafe_b64encode(value).decode("ascii").rstrip("=")


def _rp_id_hash(rp_id: str) -> bytes:
    return hashlib.sha256(rp_id.encode("idna")).digest()


def _parse_authenticator_data(data: bytes) -> dict:
    if len(data) < 37:
        abort(400, "Authenticator data too short")
    idx = 0
    rp_id_hash = data[idx : idx + 32]
    idx += 32
    flags = data[idx]
    idx += 1
    sign_count = int.from_bytes(data[idx : idx + 4], "big")
    idx += 4

    credential_id = None
    credential_public_key = None

    if flags & 0x40:
        if len(data) < idx + 18:
            abort(400, "Malformed attested credential data")
        idx += 16  # skip AAGUID
        cred_len = int.from_bytes(data[idx : idx + 2], "big")
        idx += 2
        credential_id = data[idx : idx + cred_len]
        idx += cred_len
        stream = BytesIO(data[idx:])
        decoder = cbor2.CBORDecoder(stream)
        credential_public_key = decoder.decode()

    return {
        "rp_id_hash": rp_id_hash,
        "flags": flags,
        "sign_count": sign_count,
        "credential_id": credential_id,
        "credential_public_key": credential_public_key,
    }
