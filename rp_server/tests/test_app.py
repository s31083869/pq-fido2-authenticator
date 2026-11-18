from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rp_server.app import create_app  # noqa: E402
from rp_server.config import RPSettings  # noqa: E402
from rp_server.database import Database  # noqa: E402
from rp_server.services import ensure_user, get_user, store_credential  # noqa: E402


def make_settings(tmp_path: Path) -> RPSettings:
    return RPSettings(database_url=f"sqlite:///{tmp_path / 'rp.db'}")


def test_register_options_does_not_create_user(tmp_path: Path) -> None:
    settings = make_settings(tmp_path)
    app = create_app(settings)

    response = app.test_client().post(
        "/register/options",
        json={"username": "alice", "display_name": "Alice"},
    )

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["success"] is True
    assert payload["data"]["user"]["name"] == "alice"
    assert payload["data"]["user"]["id"]

    with Database(settings).session() as session:
        assert get_user(session, "alice") is None


def test_register_options_offers_ml_dsa_then_fn_dsa_in_preference_order(
    tmp_path: Path,
) -> None:
    """Day 3 T1：預設設定下，/register/options 的 pubKeyCredParams 剛好依序宣告五個演算法。

    依據：workflow.md F03 驗收標準（pubKeyCredParams 包含 -54/-55）；D6（Decision Log 第 47 號）
    規定順序為 ML-DSA 在前、FN-DSA 在後；WebAuthn §5.4 規定 pubKeyCredParams 依 RP 偏好由高到低排列，
    authenticator 會挑第一個自己支援的，所以順序本身就是 RP 對外表達的偏好，必須完全相同。
    """
    settings = make_settings(tmp_path)
    app = create_app(settings)

    response = app.test_client().post(
        "/register/options",
        json={"username": "alice", "display_name": "Alice"},
    )

    assert response.status_code == 200
    params = response.get_json()["data"]["pubKeyCredParams"]
    # 每一筆都是 {"type": "public-key", "alg": COSE 編號}：ML-DSA-65、ML-DSA-44、ML-DSA-87、
    # FN-DSA-512（暫定 -54）、FN-DSA-1024（暫定 -55）
    assert params == [
        {"type": "public-key", "alg": -49},
        {"type": "public-key", "alg": -48},
        {"type": "public-key", "alg": -50},
        {"type": "public-key", "alg": -54},
        {"type": "public-key", "alg": -55},
    ]


def test_authenticate_options_rejects_unknown_user_without_creating_record(
    tmp_path: Path,
) -> None:
    settings = make_settings(tmp_path)
    app = create_app(settings)

    response = app.test_client().post(
        "/authenticate/options",
        json={"username": "missing"},
    )

    assert response.status_code == 400
    payload = response.get_json()
    assert payload["success"] is False
    assert payload["message"] == "Unknown user"

    with Database(settings).session() as session:
        assert get_user(session, "missing") is None


def test_authenticate_options_rejects_user_without_credentials(tmp_path: Path) -> None:
    settings = make_settings(tmp_path)
    app = create_app(settings)
    db = Database(settings)
    with db.session() as session:
        ensure_user(session, "orphan", "Orphan", user_handle="orphan-handle")

    response = app.test_client().post(
        "/authenticate/options",
        json={"username": "orphan"},
    )

    assert response.status_code == 400
    payload = response.get_json()
    assert payload["success"] is False
    assert payload["message"] == "No credential registered"


def test_authenticate_options_returns_existing_user_credentials(tmp_path: Path) -> None:
    settings = make_settings(tmp_path)
    app = create_app(settings)
    db = Database(settings)
    with db.session() as session:
        user = ensure_user(session, "alice", "Alice", user_handle="alice-handle")
        store_credential(session, user, "credential-id", "public-key", -48)

    response = app.test_client().post(
        "/authenticate/options",
        json={"username": "alice"},
    )

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["success"] is True
    assert payload["data"]["allowCredentials"] == [
        {"id": "credential-id", "type": "public-key", "transports": ["internal"]}
    ]
