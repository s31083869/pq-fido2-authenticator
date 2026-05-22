from __future__ import annotations

from base64 import urlsafe_b64decode as b64decode
import json
from types import SimpleNamespace

import cbor2
import pytest

from authenticator import Authenticator
from authenticator.models import CredentialRecord
from authenticator.service import NoopVerifier, TouchIDVerifier, WindowsHelloVerifier
from authenticator.storage import CredentialStoreError
from rp_server.services import _parse_authenticator_data


class FakeSignatureSuite:
    def __init__(self, algorithm: int) -> None:
        self.algorithm = algorithm

    def generate_keypair(self) -> SimpleNamespace:
        pub = f"public-{self.algorithm}".encode()
        priv = f"private-{self.algorithm}".encode()
        return SimpleNamespace(public_key=pub, private_key=priv)

    def sign(self, record: CredentialRecord, payload: bytes) -> bytes:
        return payload + b"::sig"


@pytest.fixture
def authenticator(monkeypatch, temp_settings) -> Authenticator:
    from authenticator import service

    monkeypatch.setattr(service, "PQCSignatureSuite", FakeSignatureSuite)
    # Force Noop verifier regardless of platform
    return Authenticator(settings=temp_settings, user_verifier=NoopVerifier())


def make_creation_options() -> dict:
    return {
        "challenge": "abc",
        "rp": {"id": "example.com", "name": "Example"},
        "user": {"id": "user-id", "name": "user", "displayName": "User"},
        "pubKeyCredParams": [{"type": "public-key", "alg": -49}],
        "timeout": 60000,
        "attestation": "none",
        "authenticatorSelection": {"userVerification": "preferred"},
        "excludeCredentials": [],
    }


def make_request_options(credential_id: str) -> dict:
    return {
        "challenge": "assertion-chal",
        "rpId": "example.com",
        "allowCredentials": [{"id": credential_id, "type": "public-key"}],
        "timeout": 60000,
        "userVerification": "preferred",
    }


def test_make_credential_produces_valid_attestation(authenticator):
    result = authenticator.make_credential(make_creation_options(), origin="https://example.com")

    response = result["response"]
    assert "attestationObject" in response
    attestation = cbor2.loads(
        _b64_to_bytes(response["attestationObject"])
    )
    assert attestation["fmt"] == "none"
    parsed = _parse_authenticator_data(attestation["authData"])
    assert parsed["credential_id"] is not None
    assert parsed["credential_public_key"][3] == -49
    assert response["transports"] == ["internal"]
    assert result["authenticatorAttachment"] == "platform"
    assert result["clientExtensionResults"] == {}
    client_data = json.loads(_b64_to_bytes(response["clientDataJSON"]))
    assert client_data["crossOrigin"] is False

    # Exclude list should now block a duplicate registration
    duplicate_options = make_creation_options()
    duplicate_options["excludeCredentials"] = [{"id": result["id"], "type": "public-key"}]
    with pytest.raises(CredentialStoreError):
        authenticator.make_credential(duplicate_options, origin="https://example.com")


def test_get_assertion_updates_sign_count(authenticator):
    creation = authenticator.make_credential(make_creation_options(), origin="https://example.com")
    assertion = authenticator.get_assertion(
        make_request_options(creation["id"]), origin="https://example.com"
    )

    response = assertion["response"]
    auth_data = _b64_to_bytes(response["authenticatorData"])
    parsed = _parse_authenticator_data(auth_data)
    assert parsed["sign_count"] == 1
    signature = _b64_to_bytes(response["signature"])
    assert signature.endswith(b"::sig")
    client_data = json.loads(_b64_to_bytes(response["clientDataJSON"]))
    assert client_data["crossOrigin"] is False
    assert assertion["authenticatorAttachment"] == "platform"
    assert assertion["clientExtensionResults"] == {}


def test_make_credential_rejects_rp_id_origin_mismatch(authenticator):
    with pytest.raises(ValueError, match="rpId mismatch"):
        authenticator.make_credential(make_creation_options(), origin="https://wrong.example.com")


def test_get_assertion_defaults_rp_id_from_origin(authenticator):
    creation = authenticator.make_credential(make_creation_options(), origin="https://example.com")
    request_options = make_request_options(creation["id"])
    request_options.pop("rpId")

    assertion = authenticator.get_assertion(request_options, origin="https://example.com")

    auth_data = _b64_to_bytes(assertion["response"]["authenticatorData"])
    parsed = _parse_authenticator_data(auth_data)
    assert parsed["sign_count"] == 1


def test_get_assertion_accepts_null_transports(authenticator):
    creation = authenticator.make_credential(make_creation_options(), origin="https://example.com")
    request_options = make_request_options(creation["id"])
    request_options["allowCredentials"][0]["transports"] = None

    assertion = authenticator.get_assertion(request_options, origin="https://example.com")

    assert assertion["id"] == creation["id"]


def test_default_user_verifier_selects_platform(monkeypatch):
    from authenticator import service

    monkeypatch.setattr(service.sys, "platform", "darwin")
    assert isinstance(Authenticator._default_user_verifier(), TouchIDVerifier)

    monkeypatch.setattr(service.sys, "platform", "win32")
    assert isinstance(Authenticator._default_user_verifier(), WindowsHelloVerifier)

    monkeypatch.setattr(service.sys, "platform", "linux")
    assert isinstance(Authenticator._default_user_verifier(), NoopVerifier)


def _b64_to_bytes(data: str) -> bytes:
    padding = "=" * (-len(data) % 4)
    return b64decode(data + padding)
