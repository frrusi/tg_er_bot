from operator import methodcaller
from typing import Iterable

from sqlalchemy import orm, or_, update
from sqlalchemy import select, ScalarResult, exc
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from tg_er_bot.models import tables


class Database:
    def __init__(self, engine: Engine):
        self.engine = engine
        tables.Base.metadata.create_all(engine)

    def _connect_session(self, *args, return_type: str = "one"):
        with Session(self.engine, expire_on_commit=False) as session, session.begin():
            try:
                return methodcaller(return_type)(session.scalars(*args))
            except exc.ResourceClosedError:
                pass

    def add_data(self, table, data: Iterable = None):
        self._connect_session(insert(table), data)

    async def is_user_blocked(self, user_id) -> bool:
        try:
            return self._connect_session(
                select(tables.User.is_blocked).where(tables.User.id == user_id)
            )
        except orm.exc.NoResultFound:
            return False

    def _upsert(self, query) -> ScalarResult:
        return self._connect_session(query)

    async def add_user(self, **kwargs) -> None:
        self._upsert(insert(tables.User).values(**kwargs).on_conflict_do_nothing(index_elements=["id"]))

    def get_currencies(self, query_text: str):
        if query_text:
            return self._connect_session(
                select(
                    tables.Currency
                ).where(
                    or_(
                        tables.Currency.Name.ilike(f"%{query_text}%"),
                        tables.Currency.CharCode.ilike(f"%{query_text}%")
                    )
                ), return_type="all")

        return self._connect_session(
            select(tables.Currency),
            return_type="all"
        )

    async def get_user_role(self, user_id: int, role: str) -> bool:
        return self._connect_session(
            select(getattr(tables.User, role)).where(tables.User.id == user_id)
        )

    async def get_admins(self):
        return self._connect_session(
            select(tables.User.id, tables.User.username).where(tables.User.is_admin)
        )

    async def set_rights(self, user_id, field, value):
        return self._connect_session(
            update(tables.User).where(tables.User.id == user_id).values(**{field: value})
        )
