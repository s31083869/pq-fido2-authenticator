from __future__ import annotations

import pytest

from authenticator.models import CredentialRecord
from authenticator.storage import CredentialStore, CredentialStoreError


def make_record() -> CredentialRecord:
    return CredentialRecord.new(
        user_handle="user-1",
        rp_id="example.com",
        algorithm=-49,
        public_key=b"public-key",
        private_key=b"private-key",
    )


def test_store_round_trip(temp_settings):
    store = CredentialStore(temp_settings)
    record = make_record()
    store.save(record)

    loaded = store.load(record.credential_id)
    assert loaded.user_handle == "user-1"
    assert loaded.rp_id == "example.com"

    all_records = store.list_all()
    assert len(all_records) == 1
    assert all_records[0].credential_id == record.credential_id

    store.delete(record.credential_id)
    with pytest.raises(CredentialStoreError):
        store.load(record.credential_id)
