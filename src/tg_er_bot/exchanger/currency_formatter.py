from currency_api_service import Currency


def format_currency(currency: Currency) -> str:
    """Formats currency data in string"""

    return f"{currency.nominal} {currency.name} = {currency.value} рублей"
