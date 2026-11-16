from __future__ import annotations

from pathlib import Path

import pytest

from authenticator.config import AuthenticatorSettings
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


def _settings(tmp_path: Path, backend: str) -> AuthenticatorSettings:
    """建立指定儲存後端的測試設定，index 與憑證資料夾都放在暫存資料夾。

    參數：
        tmp_path：pytest 提供的暫存資料夾。
        backend："file"（Windows 預設，加密檔）或 "keyring"（其他平台預設）。

    回傳：
        給 CredentialStore 使用的設定。明確指定後端，測試結果才不會因作業系統而不同。
    """
    return AuthenticatorSettings(
        keyring_service="test-service",
        credential_index_path=str(tmp_path / "index.json"),
        credential_store_backend=backend,
    )


@pytest.mark.parametrize(
    "id_kind", ["relative_slash", "relative_backslash", "absolute_path"]
)
def test_file_backend_rejects_path_like_id_before_touching_files(
    tmp_path, monkeypatch, id_kind
):
    """T12：ID 是路徑寫法時，要回報找不到，而且回報之前完全不碰檔案系統。

    依據：ID 只是識別碼，不能被當成路徑解讀（同 T8）。檢查必須在碰到檔案系統之前完成：
    load() 讀出後的 ID 比對發生在查檔、讀檔之後，那時已經碰過資料夾外的檔案；
    在 Windows 上，光是查詢「//主機/共用資料夾」是否存在就可能連線到外部主機。
    以反斜線分隔的寫法只有在 Windows 上才會被解讀成路徑，在 Linux 上它只是含反斜線的檔名。
    """
    store = CredentialStore(_settings(tmp_path, "file"))
    credential_id = {
        "relative_slash": "../outside",
        "relative_backslash": r"..\outside",
        "absolute_path": str(tmp_path / "outside"),
    }[id_kind]

    def forbidden(self, *args, **kwargs):
        raise AssertionError(f"不可以碰到檔案系統：{self}")

    # 只在 load() 執行期間，把「查詢檔案是否存在」和「讀檔」換成一被呼叫就失敗的版本
    with monkeypatch.context() as patch:
        patch.setattr(Path, "exists", forbidden)
        patch.setattr(Path, "read_bytes", forbidden)
        with pytest.raises(CredentialStoreError, match="not found"):
            store.load(credential_id)


def test_load_rejects_id_differing_only_in_case_on_case_insensitive_backend(
    tmp_path, monkeypatch
):
    """T13：儲存後端比對名稱不分大小寫時，只差大小寫的 ID 仍要回報找不到。

    依據：同 T7，credential ID 必須完全相同才算同一張憑證（WebAuthn §6.3.3；Phase-1 spec 6.2）。
    這裡用不分大小寫的假 keyring 模擬 Windows 的情況，讓 Linux 的 CI 也能偵測到
    load() 的 ID 比對被拿掉；conftest 預設的假 keyring 區分大小寫，做不到這一點。
    """
    entries: dict = {}

    def set_password(service: str, name: str, value: str) -> None:
        # 名稱一律轉成小寫再存：大小寫不同的名稱會對到同一筆
        entries[(service, name.lower())] = value

    def get_password(service: str, name: str):
        return entries.get((service, name.lower()))

    monkeypatch.setattr("authenticator.storage.keyring.set_password", set_password)
    monkeypatch.setattr("authenticator.storage.keyring.get_password", get_password)
    store = CredentialStore(_settings(tmp_path, "keyring"))
    record = make_record()
    store.save(record)
    swapped_id = record.credential_id.swapcase()

    # 前提：ID 裡有英文字母，而且假後端用大小寫互換的 ID 確實查得到 A，模擬才成立
    assert swapped_id != record.credential_id
    assert get_password("test-service", swapped_id) is not None
    # 用 A 原本的 ID 讀取時正常取得 A
    assert store.load(record.credential_id).credential_id == record.credential_id
    with pytest.raises(CredentialStoreError, match="not found"):
        store.load(swapped_id)
