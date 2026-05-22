"""Pydantic schemas for request/response payloads."""

from __future__ import annotations

from typing import List, Literal, Optional

from pydantic import BaseModel, Field


class RegisterOptionsRequest(BaseModel):
    username: str
    display_name: str


class RegisterVerifyRequest(BaseModel):
    username: str
    credential: dict


class AuthenticateOptionsRequest(BaseModel):
    username: str


class AuthenticateVerifyRequest(BaseModel):
    username: str
    credential: dict


class RPResponse(BaseModel):
    success: bool = True
    message: Optional[str] = None
    data: Optional[dict] = None


class RegisterOptionsResponse(BaseModel):
    challenge: str
    rp: dict
    user: dict
    pubKeyCredParams: List[dict]
    timeout: int
    attestation: Literal["none"] = "none"
    authenticatorSelection: dict
    extensions: dict = Field(default_factory=dict)
    excludeCredentials: List[dict] = Field(default_factory=list)


class AuthenticateOptionsResponse(BaseModel):
    challenge: str
    rpId: str
    allowCredentials: List[dict]
    timeout: int
    userVerification: Literal["preferred"] = "preferred"
