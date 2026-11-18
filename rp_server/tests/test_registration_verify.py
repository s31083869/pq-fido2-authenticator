"""RP 註冊驗證（/register/verify）的測試。

依據：WebAuthn §7.1（註冊新憑證）規定 RP 要檢查 clientDataJSON、authenticatorData 的 rpIdHash，
並確認憑證公鑰的 alg 是 RP 在 pubKeyCredParams 中提供過的演算法。

這裡不使用 authenticator 的程式：RP 和 authenticator 在協議中是不同角色（D3／Decision Log 第 57 號），
所以依 WebAuthn §6.1、§6.5 自己組出 attestationObject，公鑰則用真的 liboqs 產生。
T2 對共用演算法表的每個演算法跑「註冊 → 存進 DB → 登入驗章」；T3 確認 RP 不接受沒宣告的演算法。
"""

from __future__ import annotations

import base64
import hashlib
import secrets
import sys
from pathlib import Path

import cbor2
import oqs
import pytest
from sqlalchemy import func, select

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rp_server.app import create_app  # noqa: E402
from rp_server.config import RPSettings  # noqa: E402
from rp_server.database import Database  # noqa: E402
from rp_server.models import Credential  # noqa: E402
from shared.pq_algorithms import ALGORITHMS  # noqa: E402

# 測試用帳號；RP 的 origin 與 rp_id 用 RPSettings 的預設值（http://localhost:3000、localhost）
USERNAME = "alice"
ORIGIN = "http://localhost:3000"
RP_ID = "localhost"

# COSE_Key 的整數標籤（RFC 9052 §7、RFC 9964）：1 = kty，3 = alg，-1 = AKP 的公鑰 bytes
COSE_KTY = 1
COSE_ALG = 3
COSE_AKP_PUB = -1
# kty 的值：7 = AKP（RFC 9964，後量子公鑰），2 = EC2（橢圓曲線，用來做錯誤的情境）
KTY_AKP = 7
KTY_EC2 = 2


def _b64url(data: bytes) -> str:
    """把 bytes 轉成不補「=」的 base64url 字串，這是前端送給 RP 的格式。"""
    return base64.urlsafe_b64encode(data).decode("ascii").rstrip("=")


def _cose_key(alg: int, public_key: bytes, kty: int | None = KTY_AKP) -> dict:
    """組出 credentialPublicKey 的 COSE_Key map。

    正常情況是 AKP 格式 {1: 7, 3: alg, -1: 公鑰}（RFC 9964）。
    kty 傳入其他值可做出錯誤的金鑰類型；傳入 None 則完全不放 kty 欄位，供 T5 使用。
    """
    key: dict = {COSE_ALG: alg, COSE_AKP_PUB: public_key}
    if kty is not None:
        key[COSE_KTY] = kty
    return key


def _attestation_object(cose_key: dict, credential_id: bytes) -> bytes:
    """依 WebAuthn §6.1、§6.5 組出 fmt 為 none 的 attestationObject（CBOR bytes）。

    authData 結構：
      0–31   rpIdHash = SHA-256("localhost")
      32     flags = 0x45（UP 0x01 + UV 0x04 + AT 0x40；AT 表示後面接著 attested credential data）
      33–36  signCount = 0，大端序
      37–52  AAGUID = 16 個 0（不提供廠牌資訊）
      53–54  credentialIdLength，大端序
      55–    credentialId，接著是 CBOR 編碼的 credentialPublicKey
    """
    auth_data = (
        hashlib.sha256(RP_ID.encode("ascii")).digest()
        + bytes([0x45])
        + (0).to_bytes(4, "big")
        + bytes(16)
        + len(credential_id).to_bytes(2, "big")
        + credential_id
        + cbor2.dumps(cose_key)
    )
    return cbor2.dumps({"fmt": "none", "attStmt": {}, "authData": auth_data})


def _register(client, cose_key: dict, credential_id: bytes):
    """跑一次完整的註冊：/register/options 取得 challenge，再把組好的結果送到 /register/verify。

    clientDataJSON 的 type 為 webauthn.create、challenge 為 RP 剛發出的值、origin 為本站，
    讓除了 credentialPublicKey 以外的檢查都會通過，測試只看公鑰相關的結果。
    """
    options = client.post(
        "/register/options", json={"username": USERNAME, "display_name": "Alice"}
    )
    assert options.status_code == 200
    challenge = options.get_json()["data"]["challenge"]
    client_data_json = (
        f'{{"type":"webauthn.create","challenge":"{challenge}","origin":"{ORIGIN}"}}'
    ).encode("utf-8")
    return client.post(
        "/register/verify",
        json={
            "username": USERNAME,
            "credential": {
                "id": _b64url(credential_id),
                "rawId": _b64url(credential_id),
                "type": "public-key",
                "response": {
                    "clientDataJSON": _b64url(client_data_json),
                    "attestationObject": _b64url(
                        _attestation_object(cose_key, credential_id)
                    ),
                },
            },
        },
    )


def _credential_count(settings: RPSettings) -> int:
    """回傳 RP 資料庫中的憑證數量，用來確認被拒絕的註冊沒有留下資料。"""
    with Database(settings).session() as session:
        return session.scalar(select(func.count()).select_from(Credential))


@pytest.mark.parametrize("algorithm", ALGORITHMS, ids=lambda a: a.label)
def test_registers_and_authenticates_real_credential_for_every_registry_algorithm(
    tmp_path: Path, algorithm
) -> None:
    """T2：對共用表的每個演算法，用真的 liboqs 金鑰經過 /register/verify 註冊，再登入驗章。

    依據：workflow.md F04 驗收標準（FN-DSA credential 可被存入 DB，assertion 可驗章成功）、
    F14（註冊後保存 algorithm=-54/-55）；WebAuthn §7.1、§7.2；CLAUDE.md「真實密碼學」。
    和 test_authentication_verify.py 的 T7 不同：這裡的憑證經過 RP 真正的註冊檢查才進入 DB。
    """
    settings = RPSettings(database_url=f"sqlite:///{tmp_path / 'rp.db'}")
    client = create_app(settings).test_client()
    credential_id = secrets.token_bytes(32)

    with oqs.Signature(algorithm.oqs_name) as signer:
        public_key = signer.generate_keypair()

        # 註冊：RP 檢查通過後，以 base64url 的 credential ID 為主鍵存下 alg 與公鑰
        response = _register(
            client, _cose_key(algorithm.cose_alg, public_key), credential_id
        )
        assert response.status_code == 200, response.get_json()
        with Database(settings).session() as session:
            stored = session.get(Credential, _b64url(credential_id))
            assert stored is not None
            assert stored.algorithm == algorithm.cose_alg
            assert stored.public_key == _b64url(public_key)

        # 登入：簽章輸入是 authenticatorData ‖ SHA-256(clientDataJSON)（WebAuthn §7.2）。
        # 登入用的 authenticatorData 只有 37 bytes：rpIdHash、flags 0x05（UP + UV）、signCount 1
        options = client.post("/authenticate/options", json={"username": USERNAME})
        assert options.status_code == 200
        challenge = options.get_json()["data"]["challenge"]
        client_data_json = (
            f'{{"type":"webauthn.get","challenge":"{challenge}","origin":"{ORIGIN}"}}'
        ).encode("utf-8")
        auth_data = (
            hashlib.sha256(RP_ID.encode("ascii")).digest()
            + bytes([0x05])
            + (1).to_bytes(4, "big")
        )
        signature = signer.sign(auth_data + hashlib.sha256(client_data_json).digest())

    response = client.post(
        "/authenticate/verify",
        json={
            "username": USERNAME,
            "credential": {
                "id": _b64url(credential_id),
                "rawId": _b64url(credential_id),
                "type": "public-key",
                "response": {
                    "clientDataJSON": _b64url(client_data_json),
                    "authenticatorData": _b64url(auth_data),
                    "signature": _b64url(signature),
                },
            },
        },
    )
    assert response.status_code == 200, response.get_json()
    assert response.get_json()["success"] is True


def test_rejects_registration_with_algorithm_rp_did_not_offer(tmp_path: Path) -> None:
    """T3：RP 只宣告 ML-DSA 時，送來 alg 為 -54 的註冊要回 400 Unsupported algorithm，DB 不新增憑證。

    依據：WebAuthn §7.1，RP 必須確認憑證公鑰的 alg 是它在 pubKeyCredParams 中提供的其中一個；
    workflow.md F16（RP 未宣告 FN-DSA 就不可接受）的 RP 端。前端可以被竄改，這道檢查只能由 RP server 負責。
    公鑰用真的 Falcon-512 金鑰，確保被拒絕的原因只有 alg 沒被宣告。
    """
    settings = RPSettings(
        database_url=f"sqlite:///{tmp_path / 'rp.db'}",
        hosted_algorithms=[-49, -48, -50],
    )
    client = create_app(settings).test_client()
    with oqs.Signature("Falcon-512") as signer:
        public_key = signer.generate_keypair()

    response = _register(client, _cose_key(-54, public_key), secrets.token_bytes(32))

    assert response.status_code == 400
    assert response.get_json()["message"] == "Unsupported algorithm"
    assert _credential_count(settings) == 0
