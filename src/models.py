import enum
from datetime import datetime
from typing import Optional

from sqlalchemy import (BigInteger, Boolean, DateTime, Enum, ForeignKey,
                        Integer, String, func)
from sqlalchemy.orm import Mapped, mapped_column

from .database import Model


class Role(enum.StrEnum):
    USER = enum.auto()
    ASSISTANT = enum.auto()
    SYSTEM = enum.auto()


class User(Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(length=250))
    last_name: Mapped[Optional[str]] = mapped_column(String(length=250))
    username: Mapped[Optional[str]] = mapped_column(String(length=250))
    registration_date: Mapped[datetime] = \
        mapped_column(DateTime, default=func.now())


class Message(Model):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    role: Mapped[Role] = mapped_column(Enum(Role))
    content: Mapped[str] = mapped_column(String)
    is_in_context: Mapped[bool] = mapped_column(Boolean, default=True)
    date: Mapped[datetime] = mapped_column(DateTime, default=func.now())
