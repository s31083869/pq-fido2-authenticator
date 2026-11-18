"""Python authenticator 以真的 liboqs 選用 FN-DSA 註冊、登入的測試（Day 4 T1、T2）。

依據：workflow.md F05（authenticator 能選 -54/-55 並產出簽章）、F06（credentialPublicKey 為
{1: 7, 3: alg, -1: 公鑰}）、F15（assertion 可被對應公鑰驗章）；CLAUDE.md「真實密碼學」。

這裡不使用假的簽章器，也不 import RP 的程式：attestationObject 依 WebAuthn §6.1、§6.5 自己解析，
驗章直接呼叫 liboqs。預期的長度與 liboqs 名稱都寫死為外部數值（Falcon v1.2 第 3.11 節、D2），
不從共用表推算，避免「拿實作驗證實作」。
"""

from __future__ import annotations

import base64
import hashlib
from io import BytesIO

import cbor2
import oqs
import pytest

from authenticator import Authenticator
from authenticator.service import NoopVerifier

ORIGIN = "https://example.com"
RP_ID = "example.com"

# (COSE 編號, liboqs 名稱, 公鑰 bytes, 簽章上限 bytes)
# 公鑰長度：Falcon v1.2 第 3.11 節，公鑰 = 1 byte 標頭 + 14·n/8 bytes（n = 512 → 897，n = 1024 → 1793）。
# 簽章上限：不補滿的壓縮格式（D2，第 3.11.6 節）每次長度不同，liboqs 演算法資料表訂的上限為 752／1462。
FN_DSA_CASES = [
    (-54, "Falcon-512", 897, 752),
    (-55, "Falcon-1024", 1793, 1462),
]
CASE_IDS = ["a-FN-DSA-512", "b-FN-DSA-1024"]


def _b64url_decode(value: str) -> bytes:
    """把 authenticator 回傳的 base64url 字串（不補「=」）還原成 bytes。"""
    return base64.urlsafe_b64decode(value + "=" * (-len(value) % 4))


def _creation_options(alg: int) -> dict:
    """組出註冊參數，pubKeyCredParams 只有一個演算法，確保 authenticator 只能選它。"""
    return {
        "challenge": "registration-challenge",
        "rp": {"id": RP_ID, "name": "Example"},
        "user": {"id": "user-id", "name": "user", "displayName": "User"},
        "pubKeyCredParams": [{"type": "public-key", "alg": alg}],
        "timeout": 60000,
        "attestation": "none",
        "authenticatorSelection": {"userVerification": "preferred"},
        "excludeCredentials": [],
    }


def _credential_public_key(auth_data: bytes) -> dict:
    """從註冊的 authenticatorData 取出 credentialPublicKey（COSE_Key map）。

    結構（WebAuthn §6.1、§6.5.1）：rpIdHash 32 bytes、flags 1 byte、signCount 4 bytes、
    AAGUID 16 bytes、credentialIdLength 2 bytes（大端序）、credentialId，之後是 CBOR 編碼的 COSE_Key。
    flags 的 AT 位元（0x40）必須為 1，否則後面沒有 attested credential data。
    """
    assert auth_data[32] & 0x40, "AT flag must be set in registration authData"
    cred_len = int.from_bytes(auth_data[53:55], "big")
    return cbor2.CBORDecoder(BytesIO(auth_data[55 + cred_len :])).decode()


@pytest.fixture
def authenticator(temp_settings) -> Authenticator:
    """使用真的 PQCSignatureSuite（liboqs）與 NoopVerifier，不跳出 Windows Hello。"""
    return Authenticator(settings=temp_settings, user_verifier=NoopVerifier())


@pytest.mark.parametrize(
    ("alg", "oqs_name", "pk_len", "sig_max"), FN_DSA_CASES, ids=CASE_IDS
)
def test_make_credential_with_fn_dsa_emits_akp_cose_key(
    authenticator, alg, oqs_name, pk_len, sig_max
) -> None:
    """T1：RP 只給 -54 或 -55 時，註冊產生的 credentialPublicKey 剛好是 {1: 7, 3: alg, -1: 公鑰}。

    依據：workflow.md F05、F06；RFC 9964（AKP 金鑰類型 kty = 7，公鑰放在 -1）；
    Falcon v1.2 第 3.11 節（公鑰 897／1793 bytes）。
    """
    result = authenticator.make_credential(_creation_options(alg), origin=ORIGIN)

    response = result["response"]
    attestation = cbor2.loads(_b64url_decode(response["attestationObject"]))
    # fmt 為 none：本專案不提供廠牌證明（attStmt 為空）
    assert attestation["fmt"] == "none"
    cose_key = _credential_public_key(attestation["authData"])
    # 剛好三個欄位：kty、alg、公鑰，不能多也不能少
    assert set(cose_key) == {1, 3, -1}
    assert cose_key[1] == 7
    assert cose_key[3] == alg
    assert len(cose_key[-1]) == pk_len
    # 回應中另外提供的 publicKeyAlgorithm（WebAuthn getPublicKeyAlgorithm()）也必須一致
    assert response["publicKeyAlgorithm"] == alg


@pytest.mark.parametrize(
    ("alg", "oqs_name", "pk_len", "sig_max"), FN_DSA_CASES, ids=CASE_IDS
)
def test_get_assertion_with_fn_dsa_credential_verifies_with_falcon(
    authenticator, alg, oqs_name, pk_len, sig_max
) -> None:
    """T2：用 T1 註冊的 FN-DSA 憑證登入，簽章能用 attestation 裡的公鑰以 Falcon 驗過。

    依據：workflow.md F15；WebAuthn §6.3.3（簽章輸入為 authenticatorData ‖ SHA-256(clientDataJSON)）；
    Falcon v1.2 第 3.11.6 節與 liboqs 演算法資料表（簽章上限 752／1462 bytes）；CLAUDE.md「真實密碼學」。
    驗章用的是 liboqs 的名稱（Falcon-512／Falcon-1024），不是 authenticator 的 PQCSignatureSuite，
    確認 authenticator 真的用了對應的演算法。
    """
    creation = authenticator.make_credential(_creation_options(alg), origin=ORIGIN)
    attestation = cbor2.loads(_b64url_decode(creation["response"]["attestationObject"]))
    public_key = _credential_public_key(attestation["authData"])[-1]

    assertion = authenticator.get_assertion(
        {
            "challenge": "assertion-challenge",
            "rpId": RP_ID,
            "allowCredentials": [{"id": creation["id"], "type": "public-key"}],
            "timeout": 60000,
            "userVerification": "preferred",
        },
        origin=ORIGIN,
    )

    response = assertion["response"]
    auth_data = _b64url_decode(response["authenticatorData"])
    client_data_json = _b64url_decode(response["clientDataJSON"])
    signature = _b64url_decode(response["signature"])
    # 登入的 authenticatorData 第 33–36 bytes 是 signCount（大端序）；第一次登入為 1
    assert int.from_bytes(auth_data[33:37], "big") == 1
    # 不補滿格式的簽章長度每次不同，只能檢查不超過上限
    assert 0 < len(signature) <= sig_max
    message = auth_data + hashlib.sha256(client_data_json).digest()
    with oqs.Signature(oqs_name) as verifier:
        assert verifier.verify(message, signature, public_key) is True
