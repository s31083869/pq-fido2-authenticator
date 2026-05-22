"""Database models."""

from __future__ import annotations

from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    display_name: Mapped[str] = mapped_column(String(128))
    user_handle: Mapped[str] = mapped_column(String(32), unique=True, index=True)

    credentials: Mapped[list["Credential"]] = relationship(back_populates="user")


class Credential(Base):
    __tablename__ = "credential"

    id: Mapped[str] = mapped_column(String(128), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    public_key: Mapped[str] = mapped_column(Text)
    algorithm: Mapped[int] = mapped_column(Integer)
    sign_count: Mapped[int] = mapped_column(Integer, default=0)

    user: Mapped[User] = relationship(back_populates="credentials")
