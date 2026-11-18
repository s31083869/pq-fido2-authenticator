"""Python authenticator 依 RP 的 pubKeyCredParams 選擇演算法的測試（Day 4 T3、T4、T5）。

依據：WebAuthn §6.3.2 authenticatorMakeCredential：authenticator 用清單中「第一個自己支援的」演算法
產生金鑰；清單裡都不支援時必須回錯誤，不能自己改用別的演算法，而且這項檢查排在取得使用者同意之前。
§5.4：清單依 RP 偏好由高到低排列。workflow.md F13（演算法選擇測試）、F16（RP 沒宣告 FN-DSA 時不得選用）。
T3 測選擇結果，T4 測都不支援時拒絕，T5 測演算法檢查先於使用者驗證。

這裡只測「選哪個演算法」的流程，所以用假的簽章器（CLAUDE.md 允許單元測試用假的簽章器測流程）；
FN-DSA 的真實密碼學由 test_fn_dsa_flow.py 的 T1、T2 負責。
"""

from __future__ import annotations

import base64
from io import BytesIO
from types import SimpleNamespace

import cbor2
import pytest

from authenticator import Authenticator
from authenticator.service import NoopVerifier

ORIGIN = "https://example.com"
RP_ID = "example.com"


class FakeSignatureSuite:
    """取代 PQCSignatureSuite 的假簽章器：不呼叫 liboqs，只回傳可辨識的假金鑰。

    輸入：建構時的 COSE 編號（由 authenticator 選出）。
    輸出：generate_keypair() 回傳內容含編號的假公鑰、私鑰，讓測試快速跑完選擇流程。
    """

    def __init__(self, algorithm: int) -> None:
        """記下 authenticator 選出的 COSE 編號，供 generate_keypair() 放進假金鑰。"""
        self.algorithm = algorithm

    def generate_keypair(self) -> SimpleNamespace:
        """回傳形狀和 PQCKeyPair 相同的假金鑰對（public_key、private_key 皆為 bytes）。

        內容含 COSE 編號（例如 b"public--54"），出錯時一眼就能看出用的是哪個演算法。
        """
        return SimpleNamespace(
            public_key=f"public-{self.algorithm}".encode(),
            private_key=f"private-{self.algorithm}".encode(),
        )


@pytest.fixture
def authenticator(monkeypatch, temp_settings) -> Authenticator:
    """建立使用假簽章器與 NoopVerifier 的 authenticator，不呼叫 liboqs，也不跳出 Windows Hello。"""
    from authenticator import service

    monkeypatch.setattr(service, "PQCSignatureSuite", FakeSignatureSuite)
    return Authenticator(settings=temp_settings, user_verifier=NoopVerifier())


def _creation_options(algs: list[int]) -> dict:
    """組出註冊參數，pubKeyCredParams 依給定順序列出演算法（順序就是 RP 的偏好）。"""
    return {
        "challenge": "registration-challenge",
        "rp": {"id": RP_ID, "name": "Example"},
        "user": {"id": "user-id", "name": "user", "displayName": "User"},
        "pubKeyCredParams": [{"type": "public-key", "alg": alg} for alg in algs],
        "timeout": 60000,
        "attestation": "none",
        "authenticatorSelection": {"userVerification": "preferred"},
        "excludeCredentials": [],
    }


def _cose_alg_in_attestation(attestation_object_b64: str) -> int:
    """從 attestationObject 取出 credentialPublicKey 的 3（alg）欄位。

    authData 結構（WebAuthn §6.1）：rpIdHash 32、flags 1、signCount 4、AAGUID 16、
    credentialIdLength 2（大端序）、credentialId，之後是 CBOR 編碼的 COSE_Key。
    """
    raw = base64.urlsafe_b64decode(
        attestation_object_b64 + "=" * (-len(attestation_object_b64) % 4)
    )
    auth_data = cbor2.loads(raw)["authData"]
    cred_len = int.from_bytes(auth_data[53:55], "big")
    cose_key = cbor2.CBORDecoder(BytesIO(auth_data[55 + cred_len :])).decode()
    return cose_key[3]


@pytest.mark.parametrize(
    ("algs", "expected"),
    [
        ([-7, -54], -54),  # (a) 略過不支援的 ES256，選下一個支援的 FN-DSA-512
        ([-49, -48, -50, -54, -55], -49),  # (b) RP 預設清單：ML-DSA-65 排第一
        ([-54, -49], -54),  # (c) FN-DSA-512 被排到最前面時才會選它
        ([-49, -48, -50], -49),  # (d) RP 沒宣告 FN-DSA：絕不會選到 FN-DSA
        ([-48, -55], -48),  # (e) 清單有 FN-DSA-1024，但排在支援的 ML-DSA-44 後面
    ],
    ids=["a", "b", "c", "d", "e"],
)
def test_selects_first_supported_algorithm_in_rp_order(
    authenticator, algs: list[int], expected: int
) -> None:
    """T3：authenticator 照清單順序選第一個自己支援的演算法，不自己加入清單以外的演算法。

    依據：WebAuthn §6.3.2（第一個支援的）、§5.4（清單依 RP 偏好排序）；workflow.md F13、F16。
    同時檢查回應的 publicKeyAlgorithm 與 credentialPublicKey 的 3（alg）欄位，兩者都是 RP 會讀到的值。
    """
    result = authenticator.make_credential(_creation_options(algs), origin=ORIGIN)

    response = result["response"]
    assert response["publicKeyAlgorithm"] == expected
    assert _cose_alg_in_attestation(response["attestationObject"]) == expected


def test_rejects_when_no_offered_algorithm_is_supported(authenticator) -> None:
    """T4：清單裡都不支援（ES256 -7、RS256 -257）時拋出 ValueError，不保存任何憑證。

    依據：WebAuthn §6.3.2 第 2 步：都不支援時必須回錯誤（NotSupportedError），
    不能退回清單以外的演算法；workflow.md F13。Day 2 的 T8 只測過 [-7] 一個演算法。
    """
    with pytest.raises(ValueError, match="No supported algorithm"):
        authenticator.make_credential(_creation_options([-7, -257]), origin=ORIGIN)

    # 儲存層中沒有任何憑證：被拒絕的註冊不能留下資料
    assert authenticator.store.list_all() == []


class RecordingVerifier:
    """記錄使用者驗證被呼叫幾次的假 verifier，和 NoopVerifier 一樣一律通過、不跳出 Windows Hello。

    用途：T5 要確認「不支援的演算法在使用者驗證之前就被拒絕」，只看結果拋不拋錯分辨不出順序，
    所以記下 verify_user() 的呼叫次數。
    """

    def __init__(self) -> None:
        """呼叫次數從 0 開始。"""
        self.calls = 0

    def verify_user(self, prompt: str | None = None) -> bool:
        """模擬一次成功的使用者驗證：呼叫次數加一並回傳 True，介面和 NoopVerifier 相同。

        輸入：authenticator 要顯示給使用者的提示文字（這裡不使用）。
        """
        self.calls += 1
        return True


@pytest.mark.parametrize(
    ("algs", "expected_calls", "should_succeed"),
    [
        # (a) 不支援：在使用者驗證之前就拒絕，一次都不呼叫
        ([-7], 0, False),
        # (b) 支援：註冊成功，使用者驗證剛好一次（調整順序後沒有弄丟）
        ([-54], 1, True),
    ],
    ids=["a-unsupported-rejected-before-uv", "b-supported-uv-once"],
)
def test_checks_algorithm_before_user_verification(
    monkeypatch,
    temp_settings,
    algs: list[int],
    expected_calls: int,
    should_succeed: bool,
) -> None:
    """T5：註冊時先檢查演算法，再做使用者驗證（Windows Hello）。

    依據：WebAuthn §6.3.2 authenticatorMakeCredential：第 2 步檢查 pubKeyCredParams 中至少有一個
    支援的演算法、沒有就回 NotSupportedError，排在第 6 步取得使用者同意之前；
    演算法不支援時不應打擾使用者。(b) 確保調整順序後，支援的情況仍會做一次使用者驗證。
    """
    from authenticator import service

    monkeypatch.setattr(service, "PQCSignatureSuite", FakeSignatureSuite)
    verifier = RecordingVerifier()
    authenticator = Authenticator(settings=temp_settings, user_verifier=verifier)

    if should_succeed:
        authenticator.make_credential(_creation_options(algs), origin=ORIGIN)
    else:
        with pytest.raises(ValueError, match="No supported algorithm"):
            authenticator.make_credential(_creation_options(algs), origin=ORIGIN)

    assert verifier.calls == expected_calls
