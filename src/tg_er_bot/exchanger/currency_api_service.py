import json
import urllib.request
from json.decoder import JSONDecodeError
from urllib.error import URLError

from exceptions import ApiServiceError

EXCHANGERATES_URL = "https://www.cbr-xml-daily.ru/daily_json.js"


def get_currencies() -> list[dict]:
    """Requests exchange rates in CBR API and returns it"""

    exchangerates_response = _get_exchangerates_response()
    currencies = _parse_exchangerates_response(exchangerates_response)
    return currencies


def _get_exchangerates_response() -> str:
    try:
        return urllib.request.urlopen(EXCHANGERATES_URL).read()
    except URLError:
        raise ApiServiceError


def _parse_exchangerates_response(exchangerates_response: str) -> list[dict]:
    try:
        exchangerates_dict = json.loads(exchangerates_response)
    except JSONDecodeError:
        raise ApiServiceError

    dates = {key: exchangerates_dict[key] for key in ("Date", "PreviousDate", "Timestamp")}
    return [currency | dates for currency in exchangerates_dict["Valute"].values()]
