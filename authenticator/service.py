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


def _log(
    stage: str, event: str, req: str, level: int = logging.INFO, **fields: object
) -> None:
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
        """處理註冊（navigator.credentials.create）：產生新的金鑰對，回傳 attestation 結果。

        流程：確認 rpId 與 origin 一致 → 使用者驗證 → 檢查 excludeCredentials →
        依 pubKeyCredParams 的順序選演算法 → 產生並保存金鑰對 →
        組出 clientDataJSON、authenticatorData、attestationObject。

        參數：
            options_data：RP 的註冊參數（PublicKeyCredentialCreationOptions），
                二進位欄位已由攔截層轉成 base64url 字串。
            origin：發出請求的頁面 origin（例如 http://localhost:3000），由攔截層提供，不可省略。

        回傳：
            和瀏覽器 PublicKeyCredential 相同形狀的 dict，二進位欄位皆為 base64url 字串。
        """
        options = PublicKeyCredentialCreationOptions.model_validate(options_data)
        req_id = secrets.token_hex(4)
        # origin 是 clientDataJSON 的必要欄位，缺少時直接報錯，不填預設值
        resolved_origin = self._require_origin(origin)
        rp_id = options.rp.id
        # rpId 必須和頁面 origin 的網域相同，避免頁面替其他網站建立憑證
        self._ensure_rp_id_matches_origin(rp_id, resolved_origin)
        _log(
            "register",
            "start",
            req_id,
            user=options.user.name,
            user_handle=options.user.id,
            origin=resolved_origin,
        )
        # 使用者驗證（Windows Hello／Touch ID），失敗會丟出 UserVerificationError 中止註冊
        self._verify_user(f"Verify to register {options.user.displayName}")
        # excludeCredentials 中若有本站已存在的憑證，代表重複註冊，必須拒絕
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
        # 依 RP 偏好的順序，選第一個本 authenticator 支援的後量子演算法，並用 liboqs 產生金鑰對
        alg = self._select_algorithm(options.pubKeyCredParams)
        suite = PQCSignatureSuite(alg)
        keypair = suite.generate_keypair()
        # 建立憑證紀錄（含 32 bytes 隨機 credential ID），私鑰交給儲存層加密保存
        record = CredentialRecord.new(
            user_handle=options.user.id,
            rp_id=rp_id,
            algorithm=alg,
            public_key=keypair.public_key,
            private_key=keypair.private_key,
        )
        self.store.save(record)

        # clientDataJSON：type 為 webauthn.create，記錄 RP 的 challenge 與頁面 origin
        client_data = self._build_client_data(
            "webauthn.create", options.challenge, resolved_origin
        )
        credential_id_bytes = b64url_decode(record.credential_id)
        # 公鑰以 COSE_Key（AKP：{1: 7, 3: alg, -1: 公鑰}）格式放進 attested credential data
        credential_public_key = build_credential_public_key(record, alg)
        # 註冊時 signCount 為 0，flags 為 UP + UV + AT（0x45）
        auth_data = build_authenticator_data(
            rp_id=rp_id,
            sign_count=record.sign_count,
            credential_id=credential_id_bytes,
            credential_public_key=credential_public_key,
            user_verified=True,
        )
        # attestationObject 用 CBOR 包裝 authenticatorData，fmt 為 none（不提供廠牌證明）
        attestation_object = build_attestation_object(auth_data)

        # 二進位欄位轉成 base64url 字串，交回攔截層還原成 ArrayBuffer
        response = AuthenticatorAttestationResponse(
            clientDataJSON=encode_json_payload(client_data),
            attestationObject=b64url_encode(attestation_object),
            authenticatorData=b64url_encode(auth_data),
            publicKeyAlgorithm=alg,
            publicKey=record.public_key,
            credentialId=record.credential_id,
            transports=["internal"],
        )
        # 只有 RP 要求 credProps 擴充時才回報；本 authenticator 不建立可探索憑證，所以 rk 為 False
        include_cred_props = options.extensions.get("credProps") is True

        result = {
            "id": record.credential_id,
            "rawId": record.credential_id,
            "type": "public-key",
            "authenticatorAttachment": "platform",
            "clientExtensionResults": {"credProps": {"rk": False}}
            if include_cred_props
            else {},
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
        """處理登入（navigator.credentials.get）：用既有憑證的私鑰簽章，回傳 assertion 結果。

        流程：確認 rpId 與 origin 一致 → 使用者驗證 → 從 allowCredentials 挑選憑證 →
        signCount 加 1 → 對 authenticatorData ‖ SHA-256(clientDataJSON) 簽章。

        參數：
            options_data：RP 的登入參數（PublicKeyCredentialRequestOptions），
                二進位欄位已由攔截層轉成 base64url 字串。
            origin：發出請求的頁面 origin，由攔截層提供，不可省略。

        回傳：
            和瀏覽器 PublicKeyCredential 相同形狀的 dict，二進位欄位皆為 base64url 字串。
        """
        options = PublicKeyCredentialRequestOptions.model_validate(options_data)
        req_id = secrets.token_hex(4)
        # origin 是 clientDataJSON 的必要欄位，缺少時直接報錯，不填預設值
        resolved_origin = self._require_origin(origin)
        # RP 沒給 rpId 時，依規範使用頁面 origin 的網域；兩者必須一致
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
        # 使用者驗證（Windows Hello／Touch ID），失敗會丟出 UserVerificationError 中止登入
        self._verify_user("Verify to continue sign-in")
        # RP 有給清單時，只能用清單中屬於本站的憑證；清單為空時用本站的第一把；挑不到就拒絕這次登入
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
        # 用註冊時選定的演算法簽章
        suite = PQCSignatureSuite(record.algorithm)

        # clientDataJSON：type 為 webauthn.get。這裡算雜湊用的 bytes 必須和回傳給 RP 的
        # clientDataJSON 完全相同（同樣的緊湊格式），RP 會對收到的同一串 bytes 算雜湊
        client_data = self._build_client_data(
            "webauthn.get", options.challenge, resolved_origin
        )
        client_data_json = json.dumps(client_data, separators=(",", ":")).encode(
            "utf-8"
        )
        client_data_hash = hashlib.sha256(client_data_json).digest()

        # signCount 每次登入加 1；登入時 authenticatorData 不含公鑰，flags 為 UP + UV（0x05）
        new_sign_count = record.sign_count + 1
        auth_data_bytes = build_authenticator_data(
            rp_id=rp_id,
            sign_count=new_sign_count,
            credential_id=None,
            credential_public_key=None,
            user_verified=True,
        )
        # 簽章輸入 = authenticatorData ‖ SHA-256(clientDataJSON)，共 37 + 32 = 69 bytes
        signature = suite.sign(record, auth_data_bytes + client_data_hash)
        # 簽章成功後才保存新的 signCount，避免簽章失敗時計數器白白增加
        record.sign_count = new_sign_count
        self.store.save(record)

        # 二進位欄位轉成 base64url 字串，交回攔截層還原成 ArrayBuffer
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
        """挑出這次登入要用的憑證；挑不到時回傳 None，由呼叫端拒絕這次登入。

        規則（Phase-1 spec 6.2、WebAuthn §6.3.3）：
        - RP 有給 allowCredentials：只能從清單中挑，而且憑證必須屬於目前的 rpId；
          清單裡一把都不符合就回傳 None，不可以改用清單以外的憑證。
        - RP 沒給（清單為空）：使用這個 rpId 底下的第一把憑證。

        參數：
            allow_credentials：RP 指定這個帳號可以使用的憑證（含 credential ID）。
            rp_id：目前登入的網站識別名稱。
        """
        if allow_credentials:
            for descriptor in allow_credentials:
                # authenticator 沒有這把憑證時，load() 會丟出 CredentialStoreError，改試下一把
                try:
                    record = self.store.load(descriptor.id)
                except CredentialStoreError:
                    continue
                # 憑證綁定在註冊時的網站，屬於其他網站的憑證不能拿來登入這裡
                if record.rp_id == rp_id:
                    return record
            return None
        matches = self.store.find_by_rp(rp_id)
        return matches[0] if matches else None

    @staticmethod
    def _build_client_data(
        credential_type: str, challenge: str, origin: str
    ) -> Dict[str, object]:
        return {
            "type": credential_type,
            "challenge": challenge,
            "origin": origin,
            "crossOrigin": False,
        }

    @staticmethod
    def _require_origin(origin: Optional[str]) -> str:
        """回傳呼叫端提供的頁面 origin；缺少時丟出 ValueError，不自動填入預設值。

        origin 是 clientDataJSON 的必要欄位（WebAuthn §5.8.1），RP 靠它確認請求來自本站。
        若自動填入預設值，其他網站發出的請求也會被寫成本站的 origin，RP 的檢查就會失效。
        """
        if not origin:
            raise ValueError(
                "Missing origin: the page origin is required to build clientDataJSON"
            )
        return origin

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
