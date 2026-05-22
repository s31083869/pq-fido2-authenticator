"""PQC signature helpers built on top of liboqs-python."""

from __future__ import annotations

import logging
from typing import Dict

import oqs

from .models import CredentialRecord, b64url_decode

LOGGER = logging.getLogger(__name__)

COSE_ALG_TO_OQS: Dict[int, str] = {
    -48: "ML-DSA-44",
    -49: "ML-DSA-65",
    -50: "ML-DSA-87",
}


class PQCKeyPair:
    def __init__(self, public_key: bytes, private_key: bytes, algorithm: int):
        self.public_key = public_key
        self.private_key = private_key
        self.algorithm = algorithm


class PQCSignatureSuite:
    """Lightweight wrapper around oqs.Signature with COSE mapping."""

    def __init__(self, algorithm: int):
        if algorithm not in COSE_ALG_TO_OQS:
            raise ValueError(f"Unsupported COSE algorithm: {algorithm}")
        self.algorithm = algorithm
        self.oqs_name = COSE_ALG_TO_OQS[algorithm]

    def generate_keypair(self) -> PQCKeyPair:
        with oqs.Signature(self.oqs_name) as signer:
            public_key = signer.generate_keypair()
            private_key = signer.export_secret_key()
        LOGGER.debug("Generated %s keypair", self.oqs_name)
        return PQCKeyPair(public_key, private_key, self.algorithm)

    def sign(self, record: CredentialRecord, payload: bytes) -> bytes:
        private_key = b64url_decode(record.private_key)
        with oqs.Signature(self.oqs_name, private_key) as signer:
            return signer.sign(payload)

    def verify(self, public_key: bytes, payload: bytes, signature: bytes) -> bool:
        with oqs.Signature(self.oqs_name) as verifier:
            return bool(verifier.verify(payload, signature, public_key))
