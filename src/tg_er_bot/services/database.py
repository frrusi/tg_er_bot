from enum import Enum
from operator import methodcaller
from typing import Iterable

from sqlalchemy import or_, update
from sqlalchemy import select, exc
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from tg_er_bot.models import tables


class Returns(Enum):
    ONE = "one"
    ALL = "all"


class Execution(Enum):
    EXECUTE = "execute"
    SCALARS = "scalars"


class Database:
    def __init__(self, engine: Engine):
        self.engine = engine
        tables.Base.metadata.create_all(engine)

    def _run_session(self, *args, execute_type: Execution = Execution.EXECUTE, return_type: Returns = Returns.ONE):
        with Session(self.engine, expire_on_commit=False) as session, session.begin():
            try:
                return methodcaller(return_type.value)(methodcaller(execute_type.value, *args)(session))
            except exc.ResourceClosedError:
                pass

    def add_data(self, model, data: Iterable = None):
        table = model.__table__

        stmt = insert(model).values(data)
        on_conflict_stmt = stmt.on_conflict_do_update(index_elements=[table.c.ID],
                                                      set_={key: getattr(stmt.excluded, key.name) for key in table.c})
        self._run_session(on_conflict_stmt)

    async def is_user_blocked(self, user_id) -> bool:
        return self._run_session(
            select(tables.User.is_blocked).where(tables.User.id == user_id),
            execute_type=Execution.SCALARS
        )

    async def add_user(self, **kwargs) -> None:
        self._run_session(insert(tables.User).values(**kwargs).on_conflict_do_nothing(index_elements=["id"]))

    def get_currencies(self, query_text: str):
        if query_text:
            return self._run_session(
                select(
                    tables.Currency
                ).where(
                    or_(
                        tables.Currency.Name.ilike(f"%{query_text}%"),
                        tables.Currency.CharCode.ilike(f"%{query_text}%"))
                ),
                return_type=Returns.ALL,
                execute_type=Execution.SCALARS)

        return self._run_session(
            select(tables.Currency),
            return_type=Returns.ALL,
            execute_type=Execution.SCALARS
        )

    async def get_user_role(self, user_id: int, role: str) -> bool:
        try:
            return self._run_session(
                select(getattr(tables.User, role)).where(tables.User.id == user_id),
                execute_type=Execution.SCALARS
            )
        except exc.NoResultFound:
            return False

    async def get_admins(self):
        return self._run_session(
            select(tables.User.id, tables.User.username).where(tables.User.is_admin),
            return_type=Returns.ALL
        )

    async def set_rights(self, user_id, field, value):
        return self._run_session(
            update(tables.User).where(tables.User.id == user_id).values(**{field: value})
        )

    async def get_exchange_rates(self, currency_code):
        return self._run_session(
            select(tables.Currency.Value, tables.Currency.Nominal).where(tables.Currency.CharCode == currency_code)
        )
