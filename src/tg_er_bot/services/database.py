from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.engine import Engine

from tg_er_bot.models import tables
from tg_er_bot.models.role import UserRole


class Database:
    def __init__(self, engine: Engine):
        self.engine = engine
        tables.base.metadata.create_all(engine)

    def engine_connect(self, *args, is_return=False):
        with self.engine.connect().execution_options(autocommit=True) as connection:
            if is_return:
                return connection.execute(*args)
            connection.execute(*args)

    async def add_user(self, **kwargs) -> None:
        """Сохранение пользователя в БД"""

        self.engine_connect(
            insert(tables.User).values(**kwargs).on_conflict_do_nothing(index_elements=['id'])
        )

    async def get_user_role(self, user_id: int, role: UserRole) -> bool:
        return self.engine_connect(
            select(getattr(tables.User, role)).where(tables.User.id == user_id), is_return=True
        ).fetchone()[0]
