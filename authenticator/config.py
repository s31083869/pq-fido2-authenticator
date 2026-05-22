"""Configuration for the Python authenticator."""

from __future__ import annotations

from pathlib import Path
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings


class AuthenticatorSettings(BaseSettings):
    """Runtime settings for the authenticator."""

    keyring_service: str = Field(
        default="pq-fido2-authenticator",
        description="Service name used for macOS keychain entries",
    )
    credential_index_path: str = Field(
        default=str(
            (Path(__file__).resolve().parent / "data" / "credential_index.json").resolve()
        ),
        description="Path to the credential index file used for lookups",
    )
    credential_store_backend: Literal["auto", "keyring", "file"] = Field(
        default="auto",
        description=(
            "Credential secret storage backend. auto uses Windows DPAPI-backed "
            "files on Windows and keyring elsewhere."
        ),
    )
