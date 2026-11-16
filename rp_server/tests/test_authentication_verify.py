"""RP 登入驗章（/authenticate/verify）的測試。

依據：WebAuthn Level 2 §7.2（驗證登入斷言）規定，RP 必須對「收到的 clientDataJSON
原始 bytes」計算 SHA-256，接在 authenticatorData 後面，再用公鑰驗章。
這裡用真的 liboqs（ML-DSA-44）產生金鑰與簽章，確認 RP 的驗章流程本身正確。
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
from rp_server.services import ensure_user, store_credential  # noqa: E402

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
    """
    client, signer = rp
    challenge = _issue_challenge(client)
    # 合法的 JSON，但冒號後有空格，而且欄位順序和 RP 重組的結果不同
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
