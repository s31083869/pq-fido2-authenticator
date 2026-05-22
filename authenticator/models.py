"""Pydantic models shared across authenticator modules."""

from __future__ import annotations

import base64
import json
import secrets
from dataclasses import dataclass, field
from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field, field_validator, model_validator


def b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode("ascii").rstrip("=")


def b64url_decode(data: str) -> bytes:
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)


class RelyingPartyEntity(BaseModel):
    id: str
    name: str


class UserEntity(BaseModel):
    id: str = Field(min_length=1)
    name: str
    displayName: str


class PubKeyCredParam(BaseModel):
    type: Literal["public-key"] = "public-key"
    alg: int


class AuthenticatorSelectionCriteria(BaseModel):
    residentKey: Literal["required", "preferred", "discouraged"] = "discouraged"
    requireResidentKey: bool = False
    userVerification: Literal["required", "preferred", "discouraged"] = "preferred"


class PublicKeyCredentialCreationOptions(BaseModel):
    challenge: str
    rp: RelyingPartyEntity
    user: UserEntity
    pubKeyCredParams: List[PubKeyCredParam]
    timeout: int = 90_000
    attestation: Literal["none", "indirect", "direct"] = "none"
    authenticatorSelection: AuthenticatorSelectionCriteria = Field(
        default_factory=AuthenticatorSelectionCriteria
    )
    excludeCredentials: List[PublicKeyCredentialDescriptor] = Field(
        default_factory=list
    )
    extensions: Dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def ensure_supported_algorithm(self) -> "PublicKeyCredentialCreationOptions":
        if not self.pubKeyCredParams:
            raise ValueError("pubKeyCredParams cannot be empty")
        return self


class PublicKeyCredentialDescriptor(BaseModel):
    id: str
    type: Literal["public-key"] = "public-key"
    transports: List[str] = Field(default_factory=list)

    @field_validator("transports", mode="before")
    @classmethod
    def normalize_transports(cls, value: Any) -> List[str]:
        if value is None:
            return []
        return value


class PublicKeyCredentialRequestOptions(BaseModel):
    challenge: str
    rpId: Optional[str] = None
    timeout: int = 90_000
    userVerification: Literal["required", "preferred", "discouraged"] = "preferred"
    allowCredentials: List[PublicKeyCredentialDescriptor] = Field(default_factory=list)


class AuthenticatorResponse(BaseModel):
    clientDataJSON: str


class AuthenticatorAttestationResponse(AuthenticatorResponse):
    attestationObject: str
    authenticatorData: Optional[str] = None
    publicKeyAlgorithm: int
    publicKey: str
    credentialId: str
    transports: List[str] = Field(default_factory=list)


class AuthenticatorAssertionResponse(AuthenticatorResponse):
    authenticatorData: str
    signature: str
    userHandle: Optional[str] = None


class CredentialRecordModel(BaseModel):
    credential_id: str
    user_handle: str
    rp_id: str
    algorithm: int
    public_key: str
    private_key: str
    sign_count: int = 0

    def encode(self) -> str:
        return json.dumps(self.model_dump())

    @classmethod
    def decode(cls, data: str) -> "CredentialRecordModel":
        return cls.model_validate_json(data)


@dataclass
class CredentialRecord:
    credential_id: str
    user_handle: str
    rp_id: str
    algorithm: int
    public_key: str
    private_key: str
    sign_count: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_model(self) -> CredentialRecordModel:
        return CredentialRecordModel(
            credential_id=self.credential_id,
            user_handle=self.user_handle,
            rp_id=self.rp_id,
            algorithm=self.algorithm,
            public_key=self.public_key,
            private_key=self.private_key,
            sign_count=self.sign_count,
        )

    @classmethod
    def from_model(cls, model: CredentialRecordModel) -> "CredentialRecord":
        return cls(
            credential_id=model.credential_id,
            user_handle=model.user_handle,
            rp_id=model.rp_id,
            algorithm=model.algorithm,
            public_key=model.public_key,
            private_key=model.private_key,
            sign_count=model.sign_count,
        )

    @classmethod
    def new(
        cls,
        user_handle: str,
        rp_id: str,
        algorithm: int,
        public_key: bytes,
        private_key: bytes,
    ) -> "CredentialRecord":
        credential_id = b64url_encode(secrets.token_bytes(32))
        return cls(
            credential_id=credential_id,
            user_handle=user_handle,
            rp_id=rp_id,
            algorithm=algorithm,
            public_key=b64url_encode(public_key),
            private_key=b64url_encode(private_key),
            sign_count=0,
        )


def encode_json_payload(payload: Dict[str, Any]) -> str:
    return b64url_encode(json.dumps(payload, separators=(",", ":")).encode("utf-8"))
