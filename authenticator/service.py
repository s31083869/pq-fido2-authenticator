"""Core Authenticator implementation."""

from __future__ import annotations

import hashlib
import json
import logging
import secrets
import sys
from urllib.parse import urlparse
from typing import Dict, List, Optional

from .config import AuthenticatorSettings
from .models import (
    AuthenticatorAssertionResponse,
    AuthenticatorAttestationResponse,
    CredentialRecord,
    PublicKeyCredentialCreationOptions,
    PublicKeyCredentialDescriptor,
    PublicKeyCredentialRequestOptions,
    encode_json_payload,
    b64url_encode,
    b64url_decode,
)
from .pqcrypto import COSE_ALG_TO_OQS, PQCSignatureSuite
from .storage import CredentialStore, CredentialStoreError
from .touch import (
    NoopVerifier,
    TouchIDVerifier,
    UserVerifier,
    UserVerificationError,
    WindowsHelloVerifier,
)
from .webauthn import (
    build_attestation_object,
    build_authenticator_data,
    build_credential_public_key,
)

LOGGER = logging.getLogger(__name__)

STAGE_LABELS = {"register": "Register", "authn": "Authenticate"}
EVENT_LABELS = {
    ("register", "start"): "Processing credential creation",
    ("register", "exclude.hit"): "Credential excluded by RP",
    ("register", "success"): "Credential creation completed",
    ("authn", "start"): "Processing assertion",
    ("authn", "no_credential"): "No credential available",
    ("authn", "success"): "Assertion completed",
}


def _truncate(value: str, limit: int = 64) -> str:
    if len(value) <= limit:
        return value
    half = limit // 2
    return f"{value[:half]}…{value[-half:]}"


def _build_payload(req: str, **fields: object) -> dict[str, object]:
    payload: dict[str, object] = {"request_id": req}
    for key, value in fields.items():
        if value is None:
            continue
        if isinstance(value, str):
            payload[key] = _truncate(value)
        else:
            payload[key] = value
    return payload


def _log(stage: str, event: str, req: str, level: int = logging.INFO, **fields: object) -> None:
    stage_label = STAGE_LABELS.get(stage, stage.title())
    event_label = EVENT_LABELS.get((stage, event), event)
    payload = json.dumps(_build_payload(req, **fields), indent=2, sort_keys=True)
    message = f"[Authenticator: {stage_label}]: {event_label}\n{payload}"
    LOGGER.log(level, message)


class Authenticator:
    """Software authenticator that mimics navigator.credentials flows."""

    def __init__(
        self,
        settings: Optional[AuthenticatorSettings] = None,
        credential_store: Optional[CredentialStore] = None,
        user_verifier: Optional[UserVerifier] = None,
    ) -> None:
        self.settings = settings or AuthenticatorSettings()
        self.store = credential_store or CredentialStore(self.settings)
        if user_verifier is not None:
            self.user_verifier = user_verifier
        else:
            self.user_verifier = self._default_user_verifier()

    @staticmethod
    def _default_user_verifier() -> UserVerifier:
        if sys.platform == "darwin":
            return TouchIDVerifier()
        if sys.platform == "win32":
            return WindowsHelloVerifier()
        return NoopVerifier()

    # ------------------------------------------------------------------
    def make_credential(self, options_data: Dict, origin: Optional[str] = None) -> Dict:
        options = PublicKeyCredentialCreationOptions.model_validate(options_data)
        req_id = secrets.token_hex(4)
        resolved_origin = origin or self.settings.origin
        rp_id = options.rp.id
        self._ensure_rp_id_matches_origin(rp_id, resolved_origin)
        _log(
            "register",
            "start",
            req_id,
            user=options.user.name,
            user_handle=options.user.id,
            origin=resolved_origin,
        )
        self._verify_user(f"Verify to register {options.user.displayName}")
        try:
            self._enforce_exclude_list(options.rp.id, options.excludeCredentials)
        except CredentialStoreError:
            _log(
                "register",
                "exclude.hit",
                req_id,
                user=options.user.name,
                user_handle=options.user.id,
                level=logging.WARNING,
            )
            raise
        alg = self._select_algorithm(options.pubKeyCredParams)
        suite = PQCSignatureSuite(alg)
        keypair = suite.generate_keypair()
        record = CredentialRecord.new(
            user_handle=options.user.id,
            rp_id=rp_id,
            algorithm=alg,
            public_key=keypair.public_key,
            private_key=keypair.private_key,
        )
        self.store.save(record)

        client_data = self._build_client_data("webauthn.create", options.challenge, resolved_origin)
        credential_id_bytes = b64url_decode(record.credential_id)
        credential_public_key = build_credential_public_key(record, alg)
        auth_data = build_authenticator_data(
            rp_id=rp_id,
            sign_count=record.sign_count,
            credential_id=credential_id_bytes,
            credential_public_key=credential_public_key,
            user_verified=True,
        )
        attestation_object = build_attestation_object(auth_data)

        response = AuthenticatorAttestationResponse(
            clientDataJSON=encode_json_payload(client_data),
            attestationObject=b64url_encode(attestation_object),
            authenticatorData=b64url_encode(auth_data),
            publicKeyAlgorithm=alg,
            publicKey=record.public_key,
            credentialId=record.credential_id,
            transports=["internal"],
        )
        include_cred_props = options.extensions.get("credProps") is True

        result = {
            "id": record.credential_id,
            "rawId": record.credential_id,
            "type": "public-key",
            "authenticatorAttachment": "platform",
            "clientExtensionResults": {"credProps": {"rk": False}} if include_cred_props else {},
            "response": response.model_dump(),
        }
        _log(
            "register",
            "success",
            req_id,
            user=options.user.name,
            user_handle=options.user.id,
            credential_id=record.credential_id,
            algorithm=alg,
        )
        return result

    # ------------------------------------------------------------------
    def get_assertion(self, options_data: Dict, origin: Optional[str] = None) -> Dict:
        options = PublicKeyCredentialRequestOptions.model_validate(options_data)
        req_id = secrets.token_hex(4)
        resolved_origin = origin or self.settings.origin
        rp_id = options.rpId or self._origin_host(resolved_origin)
        self._ensure_rp_id_matches_origin(rp_id, resolved_origin)
        _log(
            "authn",
            "start",
            req_id,
            rp_id=rp_id,
            allowed=len(options.allowCredentials),
            origin=resolved_origin,
        )
        self._verify_user("Verify to continue sign-in")
        record = self._locate_credential(options.allowCredentials, rp_id)
        if record is None:
            _log(
                "authn",
                "no_credential",
                req_id,
                rp_id=rp_id,
                level=logging.WARNING,
            )
            raise CredentialStoreError("No credential available for assertion")
        suite = PQCSignatureSuite(record.algorithm)

        client_data = self._build_client_data("webauthn.get", options.challenge, resolved_origin)
        client_data_json = json.dumps(client_data, separators=(",", ":")).encode("utf-8")
        client_data_hash = hashlib.sha256(client_data_json).digest()

        new_sign_count = record.sign_count + 1
        auth_data_bytes = build_authenticator_data(
            rp_id=rp_id,
            sign_count=new_sign_count,
            credential_id=None,
            credential_public_key=None,
            user_verified=True,
        )
        signature = suite.sign(record, auth_data_bytes + client_data_hash)
        record.sign_count = new_sign_count
        self.store.save(record)

        response = AuthenticatorAssertionResponse(
            clientDataJSON=encode_json_payload(client_data),
            authenticatorData=b64url_encode(auth_data_bytes),
            signature=b64url_encode(signature),
            userHandle=record.user_handle,
        )

        result = {
            "id": record.credential_id,
            "rawId": record.credential_id,
            "type": "public-key",
            "authenticatorAttachment": "platform",
            "clientExtensionResults": {},
            "response": response.model_dump(),
        }
        _log(
            "authn",
            "success",
            req_id,
            credential_id=record.credential_id,
            sign_count=record.sign_count,
        )
        return result

    # Helpers -----------------------------------------------------------
    def _verify_user(self, prompt: str) -> None:
        try:
            self.user_verifier.verify_user(prompt)
        except UserVerificationError as exc:
            LOGGER.error("User verification failed: %s", exc)
            raise

    @staticmethod
    def _select_algorithm(params: List) -> int:
        for param in params:
            if param.alg in COSE_ALG_TO_OQS:
                return param.alg
        raise ValueError("No supported algorithm from pubKeyCredParams")

    def _locate_credential(
        self,
        allow_credentials: List[PublicKeyCredentialDescriptor],
        rp_id: str,
    ) -> Optional[CredentialRecord]:
        if allow_credentials:
            record = self.store.find_first([cred.id for cred in allow_credentials])
            if record:
                return record
        matches = self.store.find_by_rp(rp_id)
        return matches[0] if matches else None

    @staticmethod
    def _build_client_data(credential_type: str, challenge: str, origin: str) -> Dict[str, object]:
        return {
            "type": credential_type,
            "challenge": challenge,
            "origin": origin,
            "crossOrigin": False,
        }

    @staticmethod
    def _origin_host(origin: str) -> str:
        parsed = urlparse(origin)
        if not parsed.hostname:
            raise ValueError("Invalid origin")
        return parsed.hostname

    @classmethod
    def _ensure_rp_id_matches_origin(cls, rp_id: str, origin: str) -> None:
        origin_host = cls._origin_host(origin)
        if rp_id != origin_host:
            raise ValueError(f"rpId mismatch: {rp_id} vs {origin_host}")

    def _enforce_exclude_list(
        self,
        rp_id: str,
        exclude_credentials: List[PublicKeyCredentialDescriptor],
    ) -> None:
        for descriptor in exclude_credentials:
            try:
                record = self.store.load(descriptor.id)
            except CredentialStoreError:
                continue
            if record.rp_id == rp_id:
                raise CredentialStoreError("Credential creation excluded by RP")

    def list_credentials_metadata(self) -> List[Dict[str, object]]:
        entries: List[Dict[str, object]] = []
        metadata = self.store.list_metadata()
        for credential_id, info in metadata.items():
            user_handle = info.get("user_handle")
            decoded = None
            if user_handle:
                try:
                    decoded = b64url_decode(user_handle).decode("utf-8")
                except Exception:  # pragma: no cover - decoding best effort
                    decoded = None
            entries.append(
                {
                    "id": credential_id,
                    "rp_id": info.get("rp_id"),
                    "user_handle": user_handle,
                    "decoded_user_handle": decoded,
                    "last_used": info.get("last_used"),
                }
            )
        return entries
