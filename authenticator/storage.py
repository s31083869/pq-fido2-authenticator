"""Credential storage for authenticator records."""

from __future__ import annotations

import ctypes
import json
import sys
import threading
from pathlib import Path
from typing import Dict, Iterable, List, Optional

import keyring

from .config import AuthenticatorSettings
from .models import CredentialRecord, CredentialRecordModel


class CredentialStoreError(RuntimeError):
    pass


class _DATA_BLOB(ctypes.Structure):
    _fields_ = [
        ("cbData", ctypes.c_ulong),
        ("pbData", ctypes.POINTER(ctypes.c_ubyte)),
    ]


class CredentialStore:
    def __init__(self, settings: AuthenticatorSettings):
        self.settings = settings
        self.service = settings.keyring_service
        self.index_path = Path(settings.credential_index_path).expanduser()
        self.backend = self._resolve_backend(settings.credential_store_backend)
        self.file_store_path = self.index_path.parent / "credentials"
        self._lock = threading.Lock()
        self._sequence = 0
        self.index_path.parent.mkdir(parents=True, exist_ok=True)
        if self.backend == "file":
            self.file_store_path.mkdir(parents=True, exist_ok=True)
        if not self.index_path.exists():
            self._write_index({})
        self._initialize_sequence()

    @staticmethod
    def _resolve_backend(requested: str) -> str:
        if requested == "auto":
            return "file" if sys.platform == "win32" else "keyring"
        if requested in {"keyring", "file"}:
            return requested
        raise ValueError(f"Unsupported credential storage backend: {requested}")

    # Index helpers -----------------------------------------------------
    def _read_index(self) -> Dict[str, Dict[str, str]]:
        if not self.index_path.exists():
            return {}
        return json.loads(self.index_path.read_text())

    def _write_index(self, data: Dict[str, Dict[str, str]]) -> None:
        self.index_path.write_text(json.dumps(data, indent=2))

    def _update_index(self, record: CredentialRecord) -> None:
        with self._lock:
            index = self._read_index()
            index[record.credential_id] = {
                "user_handle": record.user_handle,
                "rp_id": record.rp_id,
                "last_used": self._next_sequence(),
            }
            self._write_index(index)

    def _remove_from_index(self, credential_id: str) -> None:
        with self._lock:
            index = self._read_index()
            if credential_id in index:
                index.pop(credential_id)
                self._write_index(index)

    def _initialize_sequence(self) -> None:
        with self._lock:
            index = self._read_index()
            max_seq = 0
            for metadata in index.values():
                seq = metadata.get("last_used")
                if isinstance(seq, int) and seq > max_seq:
                    max_seq = seq
            self._sequence = max_seq

    def _next_sequence(self) -> int:
        self._sequence += 1
        return self._sequence

    # CRUD --------------------------------------------------------------
    def save(self, record: CredentialRecord) -> CredentialRecord:
        serialized = record.to_model().encode()
        if self.backend == "file":
            self._save_file(record.credential_id, serialized)
        else:
            keyring.set_password(self.service, record.credential_id, serialized)
        self._update_index(record)
        return record

    def delete(self, credential_id: str) -> None:
        if self.backend == "file":
            self._credential_file(credential_id).unlink(missing_ok=True)
        else:
            keyring.delete_password(self.service, credential_id)
        self._remove_from_index(credential_id)

    def load(self, credential_id: str) -> CredentialRecord:
        if self.backend == "file":
            serialized = self._load_file(credential_id)
        else:
            serialized = keyring.get_password(self.service, credential_id)
        if serialized is None:
            raise CredentialStoreError(f"Credential {credential_id} not found")
        return CredentialRecord.from_model(CredentialRecordModel.decode(serialized))

    def list_all(self) -> List[CredentialRecord]:
        index = self._read_index()
        return [self.load(cred_id) for cred_id in index.keys()]

    def find_by_user(self, user_handle: str) -> List[CredentialRecord]:
        index = self._read_index()
        matches: List[CredentialRecord] = []
        for credential_id, metadata in index.items():
            if metadata.get("user_handle") == user_handle:
                matches.append(self.load(credential_id))
        return matches

    def find_by_rp(self, rp_id: str) -> List[CredentialRecord]:
        index = self._read_index()
        matches: List[CredentialRecord] = []
        for credential_id, metadata in index.items():
            if metadata.get("rp_id") == rp_id:
                matches.append(self.load(credential_id))
        return matches

    def find_first(self, allow_credentials: Iterable[str]) -> Optional[CredentialRecord]:
        for cred_id in allow_credentials:
            try:
                return self.load(cred_id)
            except CredentialStoreError:
                continue
        return None

    def list_metadata(self) -> Dict[str, Dict[str, str]]:
        with self._lock:
            index = self._read_index()
            return {cred_id: dict(metadata) for cred_id, metadata in index.items()}

    # File backend ------------------------------------------------------
    def _credential_file(self, credential_id: str) -> Path:
        return self.file_store_path / f"{credential_id}.bin"

    def _save_file(self, credential_id: str, serialized: str) -> None:
        encrypted = _protect_bytes(serialized.encode("utf-8"))
        self._credential_file(credential_id).write_bytes(encrypted)

    def _load_file(self, credential_id: str) -> Optional[str]:
        path = self._credential_file(credential_id)
        if not path.exists():
            return None
        return _unprotect_bytes(path.read_bytes()).decode("utf-8")


def _protect_bytes(data: bytes) -> bytes:
    if sys.platform != "win32":
        raise CredentialStoreError("File credential backend requires Windows DPAPI")

    crypt32 = ctypes.WinDLL("crypt32", use_last_error=True)
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    in_buffer = ctypes.create_string_buffer(data)
    in_blob = _DATA_BLOB(len(data), ctypes.cast(in_buffer, ctypes.POINTER(ctypes.c_ubyte)))
    out_blob = _DATA_BLOB()

    if not crypt32.CryptProtectData(
        ctypes.byref(in_blob),
        None,
        None,
        None,
        None,
        0,
        ctypes.byref(out_blob),
    ):
        raise CredentialStoreError(f"DPAPI CryptProtectData failed: {ctypes.get_last_error()}")

    try:
        return bytes(ctypes.string_at(out_blob.pbData, out_blob.cbData))
    finally:
        kernel32.LocalFree(out_blob.pbData)


def _unprotect_bytes(data: bytes) -> bytes:
    if sys.platform != "win32":
        raise CredentialStoreError("File credential backend requires Windows DPAPI")

    crypt32 = ctypes.WinDLL("crypt32", use_last_error=True)
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    in_buffer = ctypes.create_string_buffer(data)
    in_blob = _DATA_BLOB(len(data), ctypes.cast(in_buffer, ctypes.POINTER(ctypes.c_ubyte)))
    out_blob = _DATA_BLOB()

    if not crypt32.CryptUnprotectData(
        ctypes.byref(in_blob),
        None,
        None,
        None,
        None,
        0,
        ctypes.byref(out_blob),
    ):
        raise CredentialStoreError(f"DPAPI CryptUnprotectData failed: {ctypes.get_last_error()}")

    try:
        return bytes(ctypes.string_at(out_blob.pbData, out_blob.cbData))
    finally:
        kernel32.LocalFree(out_blob.pbData)
