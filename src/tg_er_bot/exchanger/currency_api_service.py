import json
import urllib.request
from dataclasses import dataclass
from json.decoder import JSONDecodeError
from urllib.error import URLError

import config
from exceptions import ApiServiceError


@dataclass(slots=True, frozen=True)
class Currency:
    id: str
    number_code: str
    char_code: str
    nominal: int
    name: str
    value: float
    previous: float


def get_currencies() -> Currency:
    """Requests exchange rates in CBR API and returns it"""

    exchangerates_response = _get_exchangerates_response()
    currency = _parse_exchangerates_response(exchangerates_response)
    return currency


def _get_exchangerates_response() -> str:
    try:
        return urllib.request.urlopen(config.EXCHANGERATES_URL).read()
    except URLError:
        raise ApiServiceError


def _parse_exchangerates_response(exchangerates_response: str) -> list[Currency]:
    try:
        openweather_dict = json.loads(exchangerates_response)
    except JSONDecodeError:
        raise ApiServiceError

    return [Currency(**currency) for currency in openweather_dict]
