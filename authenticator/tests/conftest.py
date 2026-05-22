from __future__ import annotations

from pathlib import Path
from typing import Dict, Tuple
import sys

import pytest

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
RP_ROOT = ROOT / "rp_server"
if str(RP_ROOT) not in sys.path:
    sys.path.insert(0, str(RP_ROOT))

from authenticator.config import AuthenticatorSettings  # noqa: E402


@pytest.fixture(autouse=True)
def fake_keyring(monkeypatch):
    storage: Dict[Tuple[str, str], str] = {}

    def set_password(service: str, username: str, password: str) -> None:
        storage[(service, username)] = password

    def get_password(service: str, username: str) -> str | None:
        return storage.get((service, username))

    def delete_password(service: str, username: str) -> None:
        storage.pop((service, username), None)

    monkeypatch.setattr("authenticator.storage.keyring.set_password", set_password)
    monkeypatch.setattr("authenticator.storage.keyring.get_password", get_password)
    monkeypatch.setattr("authenticator.storage.keyring.delete_password", delete_password)
    yield storage


@pytest.fixture
def temp_settings(tmp_path: Path) -> AuthenticatorSettings:
    return AuthenticatorSettings(
        keyring_service="test-service",
        credential_index_path=str(tmp_path / "index.json"),
    )
