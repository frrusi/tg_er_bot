from typing import Optional

from sqlalchemy.dialects.postgresql import TEXT, SMALLINT, INTEGER, BOOLEAN, FLOAT
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):
    type_annotation_map = {
        int: INTEGER,
        bool: BOOLEAN,
        str: TEXT,
        float: FLOAT
    }


class Currency(Base):
    __tablename__ = "currencies"

    ID: Mapped[str] = mapped_column(primary_key=True)
    NumCode: Mapped[str]
    CharCode: Mapped[str]
    Nominal: Mapped[int] = mapped_column(SMALLINT)
    Name: Mapped[str]
    Value: Mapped[float]
    Previous: Mapped[float]


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    is_bot: Mapped[bool]
    is_admin: Mapped[bool] = mapped_column(default=False)
    is_creator: Mapped[bool] = mapped_column(default=False)
    is_blocked: Mapped[bool] = mapped_column(default=False)
    first_name: Mapped[Optional[str]]
    last_name: Mapped[Optional[str]]
    username: Mapped[Optional[str]]
    language_code: Mapped[Optional[str]]
    is_premium: Mapped[bool] = mapped_column(default=False)
    added_to_attachment_menu: Mapped[bool] = mapped_column(default=False)
    can_join_groups: Mapped[bool] = mapped_column(default=False)
    can_read_all_group_messages: Mapped[bool] = mapped_column(default=False)
    supports_inline_queries: Mapped[bool] = mapped_column(default=False)
