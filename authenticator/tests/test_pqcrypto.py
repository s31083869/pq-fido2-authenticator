"""authenticator 端的演算法對照與真實密碼學測試（Day 2 的 T5 前半、T6、T8）。

authenticator 在註冊時從 RP 的 pubKeyCredParams 挑選自己支援的演算法，並用 liboqs 產生金鑰、簽章；
「自己支援哪些演算法」與「COSE 編號對到哪個 liboqs 演算法」都必須來自共用演算法表（決策 D3）。
這裡全部使用真的 liboqs，不用假的簽章器。
"""

from __future__ import annotations

import pytest

from authenticator import Authenticator
from authenticator.models import CredentialRecord, b64url_encode
from authenticator.pqcrypto import COSE_ALG_TO_OQS, PQCSignatureSuite
from authenticator.service import NoopVerifier
from shared.pq_algorithms import ALGORITHMS, cose_to_oqs_names


def test_authenticator_mapping_comes_from_shared_registry() -> None:
    """T5（authenticator 端）：COSE_ALG_TO_OQS 等於共用表的「coseAlg → oqsName」，包含 FN-DSA。

    依據：決策 D3，兩端的對照都只能來自共用表；Day 2 完成標準。
    若 authenticator 另外寫死一份，RP 和 authenticator 可能把同一個編號翻成不同演算法，
    錯誤要到登入驗章時才會出現。
    """
    assert COSE_ALG_TO_OQS == cose_to_oqs_names()
    assert COSE_ALG_TO_OQS[-54] == "Falcon-512"
    assert COSE_ALG_TO_OQS[-55] == "Falcon-1024"


@pytest.mark.parametrize("algorithm", ALGORITHMS, ids=lambda a: a.label)
def test_signature_suite_round_trip_with_real_liboqs(algorithm) -> None:
    """T6：對共用表的每個演算法，用真的 liboqs 產生金鑰 → 簽章 → 驗章。

    依據：CLAUDE.md「真實密碼學」；金鑰長度依共用表（其數值來自 FIPS 204 與 Falcon v1.2）。
    簽章長度：signatureLengthFixed 為真時（ML-DSA，FIPS 204）每次都剛好是 signatureBytes；
    為假時（FN-DSA 不補滿的壓縮格式，Falcon v1.2 第 3.11.6 節）只保證不超過 signatureBytes。
    """
    suite = PQCSignatureSuite(algorithm.cose_alg)
    keypair = suite.generate_keypair()
    assert len(keypair.public_key) == algorithm.public_key_bytes
    assert len(keypair.private_key) == algorithm.private_key_bytes

    # sign() 從憑證紀錄讀取私鑰（base64url 字串），和 authenticator 登入時的用法相同
    record = CredentialRecord(
        credential_id="test-credential",
        user_handle="user-handle",
        rp_id="example.com",
        algorithm=algorithm.cose_alg,
        public_key=b64url_encode(keypair.public_key),
        private_key=b64url_encode(keypair.private_key),
    )
    # 簽章輸入的長度和登入時相同：authenticatorData 37 bytes ‖ SHA-256(clientDataJSON) 32 bytes
    payload = bytes(range(69))
    signature = suite.sign(record, payload)

    if algorithm.signature_length_fixed:
        assert len(signature) == algorithm.signature_bytes
    else:
        assert 0 < len(signature) <= algorithm.signature_bytes
    assert suite.verify(keypair.public_key, payload, signature) is True


def test_signature_suite_rejects_algorithm_outside_registry() -> None:
    """T8（前半）：共用表以外的演算法（ES256，COSE -7）不能建立簽章器。

    依據：WebAuthn §6.3.2，authenticator 只能使用自己支援的演算法；回歸保護，
    確認改用共用表之後沒有把支援範圍放寬。
    """
    with pytest.raises(ValueError, match="Unsupported COSE algorithm"):
        PQCSignatureSuite(-7)


def test_make_credential_rejects_when_rp_offers_only_unsupported_algorithm(
    temp_settings,
) -> None:
    """T8（後半）：RP 的 pubKeyCredParams 只有 ES256（-7）時，authenticator 必須拒絕註冊。

    依據：WebAuthn §6.3.2 authenticatorMakeCredential，RP 提供的演算法都不支援時必須回錯誤，
    不能自己改用別的演算法。使用 NoopVerifier，不跳出 Windows Hello。
    """
    authenticator = Authenticator(settings=temp_settings, user_verifier=NoopVerifier())
    options = {
        "challenge": "abc",
        "rp": {"id": "example.com", "name": "Example"},
        "user": {"id": "user-id", "name": "user", "displayName": "User"},
        "pubKeyCredParams": [{"type": "public-key", "alg": -7}],
        "timeout": 60000,
        "attestation": "none",
        "authenticatorSelection": {"userVerification": "preferred"},
        "excludeCredentials": [],
    }
    with pytest.raises(ValueError, match="No supported algorithm"):
        authenticator.make_credential(options, origin="https://example.com")
