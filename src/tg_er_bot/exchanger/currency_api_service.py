import json
import urllib.request
from dataclasses import dataclass
from json.decoder import JSONDecodeError
from urllib.error import URLError

from exceptions import ApiServiceError

EXCHANGERATES_URL = "https://www.cbr-xml-daily.ru/daily_json.js"


@dataclass(slots=True, frozen=True)
class Currency:
    ID: str
    NumCode: str
    CharCode: str
    Nominal: int
    Name: str
    Value: float
    Previous: float


def get_currencies() -> list[Currency]:
    """Requests exchange rates in CBR API and returns it"""

    exchangerates_response = _get_exchangerates_response()
    currencies = _parse_exchangerates_response(exchangerates_response)
    return currencies


def _get_exchangerates_response() -> str:
    try:
        return urllib.request.urlopen(EXCHANGERATES_URL).read()
    except URLError:
        raise ApiServiceError


def _parse_exchangerates_response(exchangerates_response: str) -> list[Currency]:
    try:
        exchangerates_dict = json.loads(exchangerates_response)
    except JSONDecodeError:
        raise ApiServiceError

    return [currency for currency in exchangerates_dict["Valute"].values()]
