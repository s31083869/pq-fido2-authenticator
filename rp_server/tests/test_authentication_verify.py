"""RP 登入驗章（/authenticate/verify）的測試。

依據：WebAuthn Level 2 §7.2（驗證登入斷言）規定，RP 必須對「收到的 clientDataJSON
原始 bytes」計算 SHA-256，接在 authenticatorData 後面，再用公鑰驗章。
這裡用真的 liboqs 產生金鑰與簽章，確認 RP 的驗章流程本身正確：T1、T2 用 ML-DSA-44；
T7 對共用演算法表的每個演算法各跑一次。T5 確認 RP 的演算法對照來自共用表。
"""

from __future__ import annotations

import base64
import hashlib
import sys
from pathlib import Path
from typing import Iterator

import oqs
import pytest

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rp_server.app import create_app  # noqa: E402
from rp_server.config import RPSettings  # noqa: E402
from rp_server.database import Database  # noqa: E402
from rp_server.services import COSE_TO_OQS, ensure_user, store_credential  # noqa: E402
from shared.pq_algorithms import ALGORITHMS, cose_to_oqs_names  # noqa: E402

# 測試共用的帳號與憑證 ID；憑證 ID 只要在測試資料庫中唯一即可
USERNAME = "alice"
CREDENTIAL_ID = "test-credential"


def _b64url(data: bytes) -> str:
    """把 bytes 轉成不補「=」的 base64url 字串，這是前端送給 RP 的格式。"""
    return base64.urlsafe_b64encode(data).decode("ascii").rstrip("=")


def _login_auth_data() -> bytes:
    """組出登入用的 authenticatorData，共 37 bytes。

    結構依序為：rpIdHash（SHA-256("localhost")，32 bytes）、
    flags（0x05 = UP 0x01 + UV 0x04，1 byte）、signCount（大端序整數，4 bytes，這裡用 1）。
    """
    return (
        hashlib.sha256(b"localhost").digest() + bytes([0x05]) + (1).to_bytes(4, "big")
    )


@pytest.fixture
def rp(tmp_path: Path) -> Iterator[tuple]:
    """建立一個使用暫存資料庫的 RP，並替 alice 登記一把真正的 ML-DSA-44 公鑰。

    回傳 (Flask 測試 client, 持有對應私鑰的 liboqs 簽章器)。
    簽章器在整個測試期間保持開啟，測試結束後才釋放私鑰。
    """
    settings = RPSettings(database_url=f"sqlite:///{tmp_path / 'rp.db'}")
    app = create_app(settings)
    with oqs.Signature("ML-DSA-44") as signer:
        public_key = signer.generate_keypair()
        with Database(settings).session() as session:
            user = ensure_user(session, USERNAME, "Alice", user_handle="alice-handle")
            # -48 是 ML-DSA-44 的 COSE 演算法編號，RP 驗章時用它找出 liboqs 演算法
            store_credential(session, user, CREDENTIAL_ID, _b64url(public_key), -48)
        yield app.test_client(), signer


def _issue_challenge(client) -> str:
    """呼叫 /authenticate/options，取得 RP 這次發出的 challenge（base64url 字串）。"""
    response = client.post("/authenticate/options", json={"username": USERNAME})
    assert response.status_code == 200
    return response.get_json()["data"]["challenge"]


def _verify(client, client_data_json: bytes, auth_data: bytes, signature: bytes):
    """把一次登入結果送到 /authenticate/verify，欄位格式和前端的 serializeAssertion() 相同。"""
    return client.post(
        "/authenticate/verify",
        json={
            "username": USERNAME,
            "credential": {
                "id": CREDENTIAL_ID,
                "rawId": CREDENTIAL_ID,
                "type": "public-key",
                "response": {
                    "clientDataJSON": _b64url(client_data_json),
                    "authenticatorData": _b64url(auth_data),
                    "signature": _b64url(signature),
                },
            },
        },
    )


def test_verify_hashes_raw_client_data_json_bytes(rp) -> None:
    """T1：clientDataJSON 含有空白、欄位順序也不同時，合法的簽章仍要驗章成功。

    簽章是對這串原始 bytes 計算的。RP 如果把 JSON 解析後重新組回去再算雜湊，
    重組的 bytes 會少掉空白，雜湊就不同，合法的簽章會被誤判為無效。
    （欄位順序不同本身不會造成差異：json.loads／json.dumps 會保留順序；造成差異的是空白。）
    """
    client, signer = rp
    challenge = _issue_challenge(client)
    # 合法的 JSON，但冒號後有空格；RP 若重新序列化會去掉這些空格，bytes 就和被簽章的不同
    client_data_json = (
        f'{{"origin": "http://localhost:3000", "type": "webauthn.get", '
        f'"challenge": "{challenge}"}}'
    ).encode("utf-8")
    auth_data = _login_auth_data()
    # 簽章輸入 = authenticatorData ‖ SHA-256(clientDataJSON 的原始 bytes)
    signature = signer.sign(auth_data + hashlib.sha256(client_data_json).digest())

    response = _verify(client, client_data_json, auth_data, signature)

    assert response.status_code == 200, response.get_json()
    assert response.get_json()["success"] is True


def test_verify_rejects_tampered_client_data_json(rp) -> None:
    """T2：簽章後竄改 clientDataJSON 的 crossOrigin 欄位，必須驗章失敗。

    RP 不會檢查 crossOrigin，所以這個竄改只能靠簽章抓到。這是回歸保護：
    確認改用原始 bytes 之後，簽章仍然涵蓋 clientDataJSON 的每一個 byte。
    """
    client, signer = rp
    challenge = _issue_challenge(client)
    signed_client_data = (
        f'{{"type":"webauthn.get","challenge":"{challenge}",'
        f'"origin":"http://localhost:3000","crossOrigin":false}}'
    ).encode("utf-8")
    auth_data = _login_auth_data()
    signature = signer.sign(auth_data + hashlib.sha256(signed_client_data).digest())
    # 只把 crossOrigin 從 false 改成 true，簽章與其他內容都不變
    tampered_client_data = signed_client_data.replace(
        b'"crossOrigin":false', b'"crossOrigin":true'
    )

    response = _verify(client, tampered_client_data, auth_data, signature)

    assert response.status_code == 400
    assert response.get_json()["message"] == "Invalid signature"


def test_rp_mapping_comes_from_shared_registry() -> None:
    """T5（RP 端）：COSE_TO_OQS 等於共用表的「coseAlg → oqsName」，包含 FN-DSA。

    依據：決策 D3，兩端的對照都只能來自共用表；Day 2 完成標準。
    RP 驗章用的 liboqs 名稱必須和 authenticator 簽章時用的完全相同（交接文件第 6 節 Step 2）。
    """
    assert COSE_TO_OQS == cose_to_oqs_names()
    assert COSE_TO_OQS[-54] == "Falcon-512"
    assert COSE_TO_OQS[-55] == "Falcon-1024"


@pytest.mark.parametrize("algorithm", ALGORITHMS, ids=lambda a: a.label)
def test_verify_accepts_real_signature_for_every_registry_algorithm(
    tmp_path: Path, algorithm
) -> None:
    """T7：對共用表的每個演算法，用真的 liboqs 產生金鑰 → 簽章 → 送到 RP 的 /authenticate/verify。

    依據：CLAUDE.md「真實密碼學」（產生金鑰 → 簽章 → RP 驗章）；WebAuthn §7.2，
    RP 依註冊時保存的演算法編號選出驗章演算法，對 authenticatorData ‖ SHA-256(clientDataJSON) 驗章。
    憑證直接寫進 DB：RP 註冊目前仍只接受 hosted_algorithms 的 ML-DSA（Day 3 才開放 FN-DSA），
    這裡只測登入驗章。
    """
    settings = RPSettings(database_url=f"sqlite:///{tmp_path / 'rp.db'}")
    client = create_app(settings).test_client()
    with oqs.Signature(algorithm.oqs_name) as signer:
        public_key = signer.generate_keypair()
        with Database(settings).session() as session:
            user = ensure_user(session, USERNAME, "Alice", user_handle="alice-handle")
            # DB 存的是 COSE 編號；RP 驗章時用它查共用表，找出 liboqs 演算法
            store_credential(
                session, user, CREDENTIAL_ID, _b64url(public_key), algorithm.cose_alg
            )

        challenge = _issue_challenge(client)
        client_data_json = (
            f'{{"type":"webauthn.get","challenge":"{challenge}",'
            f'"origin":"http://localhost:3000"}}'
        ).encode("utf-8")
        auth_data = _login_auth_data()
        signature = signer.sign(auth_data + hashlib.sha256(client_data_json).digest())

    response = _verify(client, client_data_json, auth_data, signature)

    assert response.status_code == 200, response.get_json()
    assert response.get_json()["success"] is True


def test_verify_rejects_credential_with_algorithm_outside_registry(
    tmp_path: Path,
) -> None:
    """T10：DB 中憑證的演算法是 -7（ES256，不在共用表中）時，RP 回 400 Unsupported algorithm。

    依據：WebAuthn §7.2，RP 用註冊時保存的演算法驗章；不認得的演算法無法驗章，
    必須拒絕，不能改用其他演算法。簽章內容隨意，因為 RP 根本不應該走到驗章那一步。
    """
    settings = RPSettings(database_url=f"sqlite:///{tmp_path / 'rp.db'}")
    client = create_app(settings).test_client()
    with Database(settings).session() as session:
        user = ensure_user(session, USERNAME, "Alice", user_handle="alice-handle")
        store_credential(session, user, CREDENTIAL_ID, _b64url(b"es256-public-key"), -7)

    challenge = _issue_challenge(client)
    client_data_json = (
        f'{{"type":"webauthn.get","challenge":"{challenge}",'
        f'"origin":"http://localhost:3000"}}'
    ).encode("utf-8")

    response = _verify(client, client_data_json, _login_auth_data(), b"signature")

    assert response.status_code == 400
    assert response.get_json()["message"] == "Unsupported algorithm"
