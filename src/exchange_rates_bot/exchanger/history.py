from typing import Protocol, List

from currency_api_service import Currency


class CurrencyStorage(Protocol):
    """Interface for any storage saving currency"""

    def save(self, currency: Currency) -> None:
        raise NotImplementedError


class DatabaseCurrencyStorage:
    """Store currency in Database"""

    def __init__(self):
        self._init_storage()

    def save(self, currency: Currency) -> None:
        self._write(currency)

    def _init_storage(self) -> None:
        ...

    def _read_history(self) -> List[Currency]:
        ...

    def _write(self, currency: Currency) -> None:
        ...


def save_currency(currency: Currency, storage: CurrencyStorage) -> None:
    """Saves currency in the storage"""

    storage.save(currency)
