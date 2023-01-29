from dataclasses import asdict
from typing import Protocol

from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql import insert

from currency_api_service import Currency
from tg_er_bot import models
from tg_er_bot.config import load_exchanger_config
from tg_er_bot.services.database import Database


class CurrencyStorage(Protocol):
    """Interface for any storage saving currency"""

    def save(self, currency: list[Currency]) -> None:
        raise NotImplementedError


class DatabaseCurrencyStorage:
    """Store currencies in Database"""

    database_object = None

    def __init__(self):
        self._init_storage()

    def save(self, currencies: list[Currency]) -> None:
        self._write(currencies)

    def _init_storage(self) -> None:
        config = load_exchanger_config("../../../bot.ini")

        self.database_object = Database(create_engine(
            "postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}".format(**asdict(config.database))
        ))

    def _write(self, currencies: list[Currency]) -> None:
        for currency in currencies:
            query = insert(models.tables.Currency).values(**currency)

            self.database_object.engine_connect(
                query.on_conflict_do_update(index_elements=[models.tables.Currency.ID],
                                            set_=currency)
            )


def save_currency(currencies: list[Currency], storage: CurrencyStorage) -> None:
    """Saves currencies in the storage"""

    storage.save(currencies)
