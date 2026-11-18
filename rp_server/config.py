"""Pydantic based configuration for the RP server."""

from __future__ import annotations

from pathlib import Path
from typing import List

from pydantic import BaseModel, Field

DATA_DIR = Path(__file__).resolve().parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
DEFAULT_DB_PATH = DATA_DIR / "rp.db"


class RPSettings(BaseModel):
    """RP server 的全部設定，啟動時建立一次，交給 create_app() 與各個驗證函式使用。

    欄位：
        database_url：SQLAlchemy 連線字串，預設是 rp_server/data/rp.db。
        rp_id：WebAuthn 的 RP ID；authenticatorData 開頭的 rpIdHash 必須等於 SHA-256(rp_id)。
        rp_name：註冊參數 rp.name，給使用者看的網站名稱。
        origin：clientDataJSON.origin 必須等於這個值，用來擋下其他網站轉送的請求（防釣魚）。
        hosted_algorithms：RP 接受的 COSE 演算法編號，順序就是偏好，見欄位旁的說明。
    """

    database_url: str = Field(
        default=f"sqlite:///{DEFAULT_DB_PATH}",
        description="SQLAlchemy connection string used by the RP server",
    )
    rp_id: str = Field(default="localhost", description="Relying Party identifier")
    rp_name: str = Field(default="PQ RP Server", description="Human readable RP name")
    origin: str = Field(
        default="http://localhost:3000",
        description="Expected origin for clientDataJSON validation",
    )
    # RP 在演算法上唯一的開關，同時決定兩件事：
    #   1. 註冊第 2 步：/register/options 依這個順序產生 pubKeyCredParams（WebAuthn §5.4，偏好由高到低）；
    #   2. 註冊第 8 步：credentialPublicKey 的 alg 不在這裡就回 400（WebAuthn §7.1）。
    # 預設順序依 D6（Decision Log 第 47 號）：ML-DSA-65、ML-DSA-44、ML-DSA-87（RFC 9964 正式編號）在前，
    # FN-DSA-512、FN-DSA-1024（draft-ietf-cose-falcon 暫定編號 -54/-55）在後。authenticator 挑第一個
    # 自己支援的，所以預設仍會選 ML-DSA，只有清單被重排時才會選到 FN-DSA。
    hosted_algorithms: List[int] = Field(
        default_factory=lambda: [-49, -48, -50, -54, -55],
        description="COSE algorithm identifiers the RP will accept",
    )
