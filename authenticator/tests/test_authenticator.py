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
    result = authenticator.make_credential(
        make_creation_options(), origin="https://example.com"
    )

    response = result["response"]
    assert "attestationObject" in response
    attestation = cbor2.loads(_b64_to_bytes(response["attestationObject"]))
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
    duplicate_options["excludeCredentials"] = [
        {"id": result["id"], "type": "public-key"}
    ]
    with pytest.raises(CredentialStoreError):
        authenticator.make_credential(duplicate_options, origin="https://example.com")


def test_get_assertion_updates_sign_count(authenticator):
    creation = authenticator.make_credential(
        make_creation_options(), origin="https://example.com"
    )
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
        authenticator.make_credential(
            make_creation_options(), origin="https://wrong.example.com"
        )


def test_get_assertion_defaults_rp_id_from_origin(authenticator):
    creation = authenticator.make_credential(
        make_creation_options(), origin="https://example.com"
    )
    request_options = make_request_options(creation["id"])
    request_options.pop("rpId")

    assertion = authenticator.get_assertion(
        request_options, origin="https://example.com"
    )

    auth_data = _b64_to_bytes(assertion["response"]["authenticatorData"])
    parsed = _parse_authenticator_data(auth_data)
    assert parsed["sign_count"] == 1


def test_get_assertion_accepts_null_transports(authenticator):
    creation = authenticator.make_credential(
        make_creation_options(), origin="https://example.com"
    )
    request_options = make_request_options(creation["id"])
    request_options["allowCredentials"][0]["transports"] = None

    assertion = authenticator.get_assertion(
        request_options, origin="https://example.com"
    )

    assert assertion["id"] == creation["id"]


def test_default_user_verifier_selects_platform(monkeypatch):
    from authenticator import service

    monkeypatch.setattr(service.sys, "platform", "darwin")
    assert isinstance(Authenticator._default_user_verifier(), TouchIDVerifier)

    monkeypatch.setattr(service.sys, "platform", "win32")
    assert isinstance(Authenticator._default_user_verifier(), WindowsHelloVerifier)

    monkeypatch.setattr(service.sys, "platform", "linux")
    assert isinstance(Authenticator._default_user_verifier(), NoopVerifier)


def test_get_assertion_rejects_when_no_allowed_credential_is_stored(authenticator):
    """T3：allowCredentials 列出的憑證一把都不在 authenticator 裡時，必須拒絕，不能改用其他憑證。

    依據：Phase-1 spec 6.2（清單內找不到就中止）、WebAuthn §6.3.3 authenticatorGetAssertion。
    """
    # authenticator 裡只有 example.com 的憑證 A
    authenticator.make_credential(make_creation_options(), origin="https://example.com")
    # RP 的清單只允許一把 authenticator 沒有的憑證 B
    request_options = make_request_options("credential-b-not-stored")

    # 鎖定拒絕原因是「找不到可用的憑證」，避免其他原因（例如解密失敗）丟出同一種錯誤時誤判通過
    with pytest.raises(CredentialStoreError, match="No credential available"):
        authenticator.get_assertion(request_options, origin="https://example.com")


def test_get_assertion_rejects_allowed_credential_from_another_site(authenticator):
    """T4：allowCredentials 指到的憑證屬於其他網站時必須拒絕，不能拿 A 網站的鑰匙登入 B 網站。

    依據：Phase-1 spec 6.2（憑證必須在清單中，而且 rpId 相符）。
    """
    # 先在 other.com 註冊憑證 C
    other_site_options = make_creation_options()
    other_site_options["rp"] = {"id": "other.com", "name": "Other"}
    credential_c = authenticator.make_credential(
        other_site_options, origin="https://other.com"
    )
    # 登入 example.com 時，RP 的清單卻列出屬於 other.com 的憑證 C
    request_options = make_request_options(credential_c["id"])

    with pytest.raises(CredentialStoreError, match="No credential available"):
        authenticator.get_assertion(request_options, origin="https://example.com")


def test_get_assertion_uses_site_credential_when_allow_list_is_empty(authenticator):
    """T5：allowCredentials 為空時，使用這個網站已存的憑證（回歸保護）。

    依據：Phase-1 spec 6.2（清單為空時，依 rpId 選第一把憑證）。
    """
    creation = authenticator.make_credential(
        make_creation_options(), origin="https://example.com"
    )
    request_options = make_request_options(creation["id"])
    request_options["allowCredentials"] = []

    assertion = authenticator.get_assertion(
        request_options, origin="https://example.com"
    )

    assert assertion["id"] == creation["id"]


@pytest.mark.parametrize("operation", ["make_credential", "get_assertion"])
def test_missing_origin_raises_clear_error(authenticator, operation):
    """T6：呼叫時沒有提供 origin，要丟出指明缺少 origin 的 ValueError，而不是看不懂的 AttributeError。

    依據：WebAuthn §5.8.1，origin 是 clientDataJSON 的必要欄位，沒有它就無法產生 clientDataJSON；
    也不能自動填入預設值，否則其他網站的請求會被寫成本站的 origin。
    """
    options = (
        make_creation_options()
        if operation == "make_credential"
        else make_request_options("any-credential")
    )

    # 訊息必須以「Missing origin」開頭：只比對「origin」不夠，_origin_host() 的「Invalid origin」也會符合
    with pytest.raises(ValueError, match="^Missing origin"):
        getattr(authenticator, operation)(options)


def test_get_assertion_rejects_allowed_id_differing_only_in_case(authenticator):
    """T7：allowCredentials 的 ID 和已存憑證 A 只差在大小寫時，必須拒絕，不能選中 A。

    依據：credential ID 是不透明的 bytes，必須完全相同才算同一張憑證（WebAuthn §6.3.3、
    Phase-1 spec 6.2）。Windows 的檔案系統比對檔名時不分大小寫，不能讓它決定比對結果。
    只有 Windows 的 file 儲存後端會重現這個問題。CI 的 Linux 改用 keyring 儲存，測試用的假 keyring
    區分大小寫，所以這個測試在 CI 上只能保護挑選憑證的流程，偵測不到大小寫問題。
    """
    creation = authenticator.make_credential(
        make_creation_options(), origin="https://example.com"
    )
    swapped_id = creation["id"].swapcase()
    # 確認 ID 裡有英文字母，大小寫互換後確實是另一個 ID
    assert swapped_id != creation["id"]
    request_options = make_request_options(swapped_id)

    with pytest.raises(CredentialStoreError, match="No credential available"):
        authenticator.get_assertion(request_options, origin="https://example.com")


def test_get_assertion_rejects_allowed_id_containing_a_path(authenticator):
    """T8：allowCredentials 的 ID 含有路徑（../credentials/<A 的 ID>）時，必須拒絕。

    依據：同 T7。ID 只是識別碼，不能被當成檔案路徑解讀，否則可以繞路開到清單以外的憑證檔。
    """
    creation = authenticator.make_credential(
        make_creation_options(), origin="https://example.com"
    )
    request_options = make_request_options(f"../credentials/{creation['id']}")

    with pytest.raises(CredentialStoreError, match="No credential available"):
        authenticator.get_assertion(request_options, origin="https://example.com")


def test_make_credential_ignores_exclude_id_differing_only_in_case(authenticator):
    """T9：excludeCredentials 的 ID 和已存憑證 A 只差在大小寫時，不可誤判為重複註冊，註冊應成功。

    依據：WebAuthn §6.3.2 authenticatorMakeCredential 依 credential ID 查找 excludeCredentials，
    必須完全相同才算 authenticator 已經擁有這張憑證。
    """
    existing = authenticator.make_credential(
        make_creation_options(), origin="https://example.com"
    )
    options = make_creation_options()
    options["excludeCredentials"] = [
        {"id": existing["id"].swapcase(), "type": "public-key"}
    ]

    result = authenticator.make_credential(options, origin="https://example.com")

    # 註冊成功，而且建立的是一張新的憑證
    assert result["id"] != existing["id"]


def _b64_to_bytes(data: str) -> bytes:
    padding = "=" * (-len(data) % 4)
    return b64decode(data + padding)
