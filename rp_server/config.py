"""Pydantic based configuration for the RP server."""

from __future__ import annotations

from pathlib import Path
from typing import List

from pydantic import BaseModel, Field

DATA_DIR = Path(__file__).resolve().parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
DEFAULT_DB_PATH = DATA_DIR / "rp.db"


class RPSettings(BaseModel):
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
    hosted_algorithms: List[int] = Field(
        default_factory=lambda: [-49, -48, -50],
        description="COSE algorithm identifiers the RP will accept",
    )
