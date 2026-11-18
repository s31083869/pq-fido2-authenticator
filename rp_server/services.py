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

from shared.pq_algorithms import ALGORITHMS, cose_to_oqs_names

from .config import RPSettings
from .models import Credential, User


ALPHABET = string.ascii_letters + string.digits

# COSE_Key 的 kty 值 7 = AKP（Algorithm Key Pair，RFC 9964），後量子公鑰使用的金鑰類型
COSE_KTY_AKP = 7

# COSE 演算法編號 → 公鑰長度（bytes），從共用演算法表產生（D3），註冊時檢查公鑰長度用
COSE_TO_PUBLIC_KEY_BYTES = {
    algorithm.cose_alg: algorithm.public_key_bytes for algorithm in ALGORITHMS
}


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
    return list(
        session.scalars(select(Credential).where(Credential.user_id == user.id))
    )


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
    """驗證一次註冊（attestation）的結果，通過時回傳要存進 DB 的憑證資料。

    依 WebAuthn §7.1 依序檢查：clientDataJSON 的 type／challenge／origin、authenticatorData 的
    rpIdHash、attested credential data 是否存在、憑證公鑰的 alg 是 RP 宣告過的。
    接著檢查公鑰本身的格式：kty 必須是 AKP（RFC 9964；kty 為必填欄位，RFC 9052 §7），
    公鑰長度必須等於共用演算法表中該演算法的 publicKeyBytes。以上任何一項不符都以 400 中止
    （輸入本身無法解析，例如 CBOR 格式錯誤時，目前會是 500，見 Day 3 待辦清單）。
    attestation 格式為 none，所以這裡不驗簽章，也無法確認 authenticator 真的持有對應的私鑰；
    公鑰檢查擋的是「格式錯誤的公鑰」，避免它存進 DB 後要到登入時才失敗。

    參數：
        payload：前端送來的註冊結果，response 裡有 clientDataJSON 與 attestationObject（base64url）。
        challenge：RP 這次發出、尚未使用過的 challenge。
        settings：RP 設定，提供 rp_id、origin 與 hosted_algorithms。

    回傳：(credential ID 的 base64url, COSE 演算法編號, 公鑰的 base64url)。
    """
    response = payload.get("response", {})
    client_data_json = _b64url_to_bytes(response.get("clientDataJSON"))
    client_data = json.loads(client_data_json)
    # type 必須是註冊；challenge 必須是剛發出的那一個（防重放）；origin 必須是本站（防釣魚）
    if client_data.get("type") != "webauthn.create":
        abort(400, "Invalid clientData type")
    if client_data.get("challenge") != challenge:
        abort(400, "Challenge mismatch")
    if client_data.get("origin") != settings.origin:
        abort(400, "Origin mismatch")

    # attestationObject 是 CBOR map {"fmt", "attStmt", "authData"}；本專案的 fmt 為 none，只取 authData
    attestation_b64 = response.get("attestationObject")
    if not attestation_b64:
        abort(400, "Missing attestationObject")
    attestation = cbor2.loads(_b64url_to_bytes(attestation_b64))
    auth_data_bytes = attestation.get("authData")
    if not isinstance(auth_data_bytes, (bytes, bytearray)):
        abort(400, "Invalid authenticator data")
    # authData 開頭 32 bytes 是 SHA-256(rpId)，確認 authenticator 是替本站建立憑證
    parsed = _parse_authenticator_data(bytes(auth_data_bytes))
    if parsed.get("rp_id_hash") != _rp_id_hash(settings.rp_id):
        abort(400, "rpId hash mismatch")
    # 註冊時 flags 的 AT 位元必須為 1，authData 後段才會有 credential ID 與 credentialPublicKey
    credential_id = parsed.get("credential_id")
    credential_public_key = parsed.get("credential_public_key")
    if credential_id is None or credential_public_key is None:
        abort(400, "Missing attested credential data")

    # COSE_Key 的 3（alg）：必須是 RP 在 pubKeyCredParams 宣告過的演算法（WebAuthn §7.1）。
    # 比對的是 RP 自己的設定，不是前端送來的清單，因為前端可以被竄改。
    algorithm = credential_public_key.get(3)
    if algorithm not in settings.hosted_algorithms:
        abort(400, "Unsupported algorithm")

    # COSE_Key 的 1（kty）：後量子公鑰使用 AKP（kty = 7，RFC 9964）；kty 是必填欄位（RFC 9052 §7），
    # 缺少或是其他類型（例如 2 = EC2）都代表這不是本專案能驗章的公鑰格式
    if credential_public_key.get(1) != COSE_KTY_AKP:
        abort(400, "Invalid public key")

    # COSE_Key 的 -1（AKP 的 pub）：公鑰本身必須是 bytes，且長度等於共用表中該演算法的 publicKeyBytes。
    # ML-DSA 與 FN-DSA 的公鑰長度都是固定的；長度錯的公鑰若存進 DB，登入時太短會驗章失敗、
    # 太長會讓 liboqs-python 丟出 ValueError。alg 不在共用表時查不到長度（get 回傳 None），一律視為不符。
    public_key_bytes = credential_public_key.get(-1)
    if not isinstance(public_key_bytes, (bytes, bytearray)):
        abort(400, "Invalid public key")
    if len(public_key_bytes) != COSE_TO_PUBLIC_KEY_BYTES.get(algorithm):
        abort(400, "Invalid public key")

    # 存進 DB 的 credential ID 與公鑰都轉成 base64url 字串
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
    """驗證一次登入（assertion）的結果，通過時回傳已更新 signCount 的憑證。

    依 WebAuthn §7.2 依序檢查：憑證屬於這個使用者、clientDataJSON 的 type／challenge／origin、
    authenticatorData 的 rpIdHash，最後用資料庫裡的公鑰驗章。任何一項不符都以 400 中止。

    參數：
        session：資料庫連線，用來查詢憑證。
        payload：前端送來的登入結果，包含 id 與 response 裡的 clientDataJSON、
            authenticatorData、signature（皆為 base64url 字串）。
        challenge：RP 這次發出、尚未使用過的 challenge。
        settings：RP 設定，提供 rp_id 與 origin。
        user：要登入的使用者。
    """
    response = payload.get("response", {})

    # 依 credential ID 找出註冊時保存的公鑰與演算法，並確認這把憑證屬於這個使用者
    credential_id = payload.get("id") or payload.get("rawId")
    credential = session.get(Credential, credential_id or "")
    if not credential or credential.user_id != user.id:
        abort(400, "Unknown credential")

    # 保留 clientDataJSON 的原始 bytes：簽章是對這串 bytes 計算的，之後要直接拿它算雜湊
    client_data_json = _b64url_to_bytes(response.get("clientDataJSON"))
    client_data = json.loads(client_data_json)
    # type 必須是登入；challenge 必須是剛發出的那一個（防重放）；origin 必須是本站（防釣魚）
    if client_data.get("type") != "webauthn.get":
        abort(400, "Invalid clientData type")
    if client_data.get("challenge") != challenge:
        abort(400, "Challenge mismatch")
    if client_data.get("origin") != settings.origin:
        abort(400, "Origin mismatch")

    # authenticatorData 開頭 32 bytes 是 SHA-256(rpId)，確認 authenticator 認定的網站就是本站
    auth_data_bytes = _b64url_to_bytes(response.get("authenticatorData"))
    parsed = _parse_authenticator_data(auth_data_bytes)
    if parsed.get("rp_id_hash") != _rp_id_hash(settings.rp_id):
        abort(400, "rpId hash mismatch")

    # 重組簽章輸入：authenticatorData ‖ SHA-256(clientDataJSON 原始 bytes)。
    # 不能把 JSON 解析後重新序列化：重新序列化會改變空白與跳脫字元的寫法、合併重複欄位，
    # bytes 就和被簽章的內容不同（欄位順序則會被 json.loads／json.dumps 保留）。
    message = auth_data_bytes + hashlib.sha256(client_data_json).digest()
    signature = _b64url_to_bytes(response.get("signature"))

    # 依註冊時保存的 COSE 演算法編號選出 liboqs 演算法，再用公鑰驗章
    oqs_alg = _cose_to_oqs(credential.algorithm)
    with oqs.Signature(oqs_alg) as verifier:
        valid = verifier.verify(
            message, signature, _b64url_to_bytes(credential.public_key)
        )
    if not valid:
        abort(400, "Invalid signature")

    # 記下這次 authenticatorData 中的 signCount（尚未檢查是否遞增，列在待辦清單）
    credential.sign_count = parsed.get("sign_count", credential.sign_count)
    return credential


# COSE 演算法編號 → liboqs 演算法名稱，從共用演算法表 shared/pq-algorithms.json 產生（決策 D3），
# 確保和 authenticator 簽章時用的名稱完全相同；兩邊不一致時，合法的簽章也會驗章失敗。
# 這張表只決定「驗章時能翻譯哪些編號」；RP 對外宣告、註冊時接受哪些演算法，
# 仍由 config.py 的 hosted_algorithms 決定。
COSE_TO_OQS = cose_to_oqs_names()


def _cose_to_oqs(alg: int) -> str:
    """把 DB 中保存的 COSE 演算法編號翻成 liboqs 演算法名稱，供登入驗章建立驗章器。

    輸入：註冊時從 credentialPublicKey 的 3（alg）欄位取得並存進 DB 的編號，例如 -54。
    輸出：liboqs 名稱，例如 Falcon-512。
    編號不在共用演算法表中時，回應 400「Unsupported algorithm」，不嘗試驗章。
    """
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
