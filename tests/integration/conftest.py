"""跨元件整合測試共用的 fixture：真的 RP（Flask test client）＋ 真的 Python authenticator。

整合測試把 authenticator 實際產生的輸出原封不動交給 RP 驗證，抓「兩邊各自都對，接起來卻不對」的問題
（例如欄位名稱、base64url 編碼不一致）。為了不碰使用者的資料：
- 測試用的 RP 資料庫放在 pytest 的暫存資料夾，註冊與登入的資料列都只寫進這裡。
  注意：`import rp_server.app` 時，模組最後一行的 `app = create_app()` 會以預設設定開啟
  rp_server/data/rp.db 並確認資料表存在（只建表、不寫資料列）。這是 Day 5 之前就有的行為，
  rp_server/tests 也一樣，已記入 Day 5 待辦清單；
- authenticator 的私鑰與憑證索引都放在 pytest 的暫存資料夾：Windows 上預設的 auto 後端是
  DPAPI 加密檔，存在索引檔旁的 credentials/；其他平台（例如 CI 的 Ubuntu）用 keyring，
  由下面的 fake_keyring 換成記憶體版；
- 使用者驗證一律用 NoopVerifier，不跳出 Windows Hello（CLAUDE.md「環境注意事項」）。
"""

from __future__ import annotations

from pathlib import Path
from typing import Callable, Dict, List, Tuple
import sys

import pytest

# 讓 authenticator、rp_server、shared 三個套件都能從專案根目錄 import（和各元件測試的做法相同）
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from authenticator import Authenticator  # noqa: E402
from authenticator.config import AuthenticatorSettings  # noqa: E402
from authenticator.service import NoopVerifier  # noqa: E402
from rp_server.app import create_app  # noqa: E402
from rp_server.config import RPSettings  # noqa: E402


@pytest.fixture(autouse=True)
def fake_keyring(monkeypatch) -> Dict[Tuple[str, str], str]:
    """把 authenticator 用來保存私鑰的 keyring 換成記憶體裡的 dict。

    為什麼：keyring 後端會寫進作業系統的密碼庫，測試不能寫進使用者的系統。
    authenticator 的 auto 後端只在非 Windows 平台使用 keyring（authenticator/storage.py 的
    _resolve_backend()），所以這個替換實際上在 CI（Ubuntu）生效；Windows 上私鑰改存 DPAPI 加密檔，
    位置在暫存資料夾，見 authenticator fixture。
    輸入：pytest 的 monkeypatch。輸出：保存內容的 dict，key 為 (service, username)。
    """
    storage: Dict[Tuple[str, str], str] = {}

    def set_password(service: str, username: str, password: str) -> None:
        storage[(service, username)] = password

    def get_password(service: str, username: str) -> str | None:
        return storage.get((service, username))

    def delete_password(service: str, username: str) -> None:
        storage.pop((service, username), None)

    monkeypatch.setattr("authenticator.storage.keyring.set_password", set_password)
    monkeypatch.setattr("authenticator.storage.keyring.get_password", get_password)
    monkeypatch.setattr(
        "authenticator.storage.keyring.delete_password", delete_password
    )
    return storage


@pytest.fixture
def authenticator(tmp_path: Path) -> Authenticator:
    """真的 Python authenticator：真的 liboqs 簽章器、NoopVerifier、暫存的憑證索引檔。

    輸入：pytest 的暫存資料夾。輸出：可直接呼叫 make_credential／get_assertion 的 Authenticator。
    """
    settings = AuthenticatorSettings(
        keyring_service="integration-test",
        credential_index_path=str(tmp_path / "authenticator-index.json"),
    )
    return Authenticator(settings=settings, user_verifier=NoopVerifier())


@pytest.fixture
def make_rp(tmp_path: Path) -> Callable[..., Tuple[object, RPSettings]]:
    """建立 RP 的工廠：可以指定 hosted_algorithms，其餘設定沿用 RP 預設值。

    RP 預設 rp_id 為 localhost、origin 為 http://localhost:3000，和 Python 路線實際執行時相同。
    輸入（呼叫工廠時）：hosted_algorithms，None 表示用 RP 預設的 [-49, -48, -50, -54, -55]。
    輸出：(Flask test client, RPSettings)；RPSettings 用來在測試裡直接查 DB。
    """

    def _make(hosted_algorithms: List[int] | None = None):
        fields: dict = {"database_url": f"sqlite:///{tmp_path / 'rp.db'}"}
        if hosted_algorithms is not None:
            fields["hosted_algorithms"] = hosted_algorithms
        settings = RPSettings(**fields)
        return create_app(settings).test_client(), settings

    return _make
