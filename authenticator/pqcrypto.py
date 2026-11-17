"""PQC signature helpers built on top of liboqs-python."""

from __future__ import annotations

import logging
from typing import Dict

import oqs

from shared.pq_algorithms import cose_to_oqs_names

from .models import CredentialRecord, b64url_decode

LOGGER = logging.getLogger(__name__)

# COSE 演算法編號 → liboqs 演算法名稱，從共用演算法表 shared/pq-algorithms.json 產生（決策 D3），
# 不在這裡寫死，確保和 RP 驗章時用的名稱完全相同。
# 這張表同時決定 authenticator「支援哪些演算法」：service.py 的 _select_algorithm()
# 只會從 RP 的 pubKeyCredParams 中挑出這裡有的編號。
COSE_ALG_TO_OQS: Dict[int, str] = cose_to_oqs_names()


class PQCKeyPair:
    def __init__(self, public_key: bytes, private_key: bytes, algorithm: int):
        self.public_key = public_key
        self.private_key = private_key
        self.algorithm = algorithm


class PQCSignatureSuite:
    """把一個 COSE 演算法編號包成 liboqs 的產生金鑰、簽章、驗章操作。

    為什麼需要：WebAuthn 只用 COSE 編號（例如 -54）表示演算法，liboqs 卻要用名稱（例如 Falcon-512）
    建立簽章器；這個類別負責翻譯，讓呼叫端只需要處理 COSE 編號。
    輸入：建構時給 COSE 編號；不在共用演算法表中的編號（例如 ES256 的 -7）拋出 ValueError。
    """

    def __init__(self, algorithm: int):
        """依 COSE 編號找出 liboqs 名稱，存在 self.oqs_name 供之後的操作使用。

        輸入：COSE 演算法編號，例如 -54。
        不在共用演算法表中時拋出 ValueError，讓呼叫端在產生金鑰之前就知道不支援。
        """
        if algorithm not in COSE_ALG_TO_OQS:
            raise ValueError(f"Unsupported COSE algorithm: {algorithm}")
        self.algorithm = algorithm
        self.oqs_name = COSE_ALG_TO_OQS[algorithm]

    def generate_keypair(self) -> PQCKeyPair:
        """產生一對新的金鑰，用於註冊。

        輸出：PQCKeyPair，內含原始的公鑰 bytes（之後放進 credentialPublicKey 的 -1 欄位）
        與私鑰 bytes（由 authenticator 加密保存，不會離開 authenticator）。
        """
        with oqs.Signature(self.oqs_name) as signer:
            public_key = signer.generate_keypair()
            private_key = signer.export_secret_key()
        LOGGER.debug("Generated %s keypair", self.oqs_name)
        return PQCKeyPair(public_key, private_key, self.algorithm)

    def sign(self, record: CredentialRecord, payload: bytes) -> bytes:
        """用憑證紀錄中的私鑰對 payload 簽章，用於登入。

        輸入：record.private_key 是 base64url 字串；payload 是 authenticatorData ‖ SHA-256(clientDataJSON)。
        輸出：簽章 bytes。ML-DSA 的長度固定；FN-DSA 每次長度不同，但不超過共用表的 signatureBytes。
        """
        private_key = b64url_decode(record.private_key)
        with oqs.Signature(self.oqs_name, private_key) as signer:
            return signer.sign(payload)

    def verify(self, public_key: bytes, payload: bytes, signature: bytes) -> bool:
        """用公鑰驗證簽章，回傳是否有效。authenticator 本身的流程不會呼叫，供測試確認簽章正確。"""
        with oqs.Signature(self.oqs_name) as verifier:
            return bool(verifier.verify(payload, signature, public_key))
