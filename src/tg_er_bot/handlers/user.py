from _decimal import Decimal

import sqlalchemy.exc
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import Message, InlineQuery, InlineQueryResultArticle, InputTextMessageContent

from tg_er_bot.services.database import Database


async def user_start(message: Message, db: Database, state: FSMContext):
    await state.reset_state()
    await db.add_user(**message.from_user.values)
    await message.reply(f"Привет, {message.from_user.first_name}!")


async def inline_handler(query: InlineQuery, db: Database):
    currencies = db.get_currencies(query.query)

    articles = [InlineQueryResultArticle(
        id=currency.ID,
        title=currency.CharCode,
        description=f"{currency.Nominal} {currency.Name} = {currency.Value} ₽",
        input_message_content=InputTextMessageContent(
            message_text=f"<b>{currency.Date.strftime('%d/%m/%Y')}</b>:\n"
                         f"{currency.Nominal} {currency.Name} = {currency.Value} ₽\n\n"
                         f"<b>{currency.PreviousDate.strftime('%d/%m/%Y')}</b>:\n"
                         f"{currency.Nominal} {currency.Name} = {currency.Previous} ₽"
        )
    ) for currency in currencies]

    await query.answer(articles, cache_time=60, is_personal=True)


def _get_conversion_result(quantity: str, currency_rate: float, nominal: int, sign: str) -> str:
    match sign:
        case '*':
            return str((Decimal(quantity) * (Decimal(currency_rate) / nominal)).quantize(Decimal("1.0000")))
        case '/':
            return str((Decimal(quantity) / (Decimal(currency_rate) / nominal)).quantize(Decimal("1.0000")))


async def _convert_currency(quantity: str, currency_code: str, sign: str, db: Database):
    try:
        currency_rate, nominal = await db.get_exchange_rates(currency_code)
    except sqlalchemy.exc.NoResultFound:
        return "Валюта не найдена"

    return _get_conversion_result(quantity, currency_rate, nominal, sign)


async def convert_from_rubles(message: Message, db: Database):
    try:
        quantity, currency_code = message.get_args().split()
    except ValueError:
        await message.reply("/from quantity currency [USD, EUR, etc.]")
        return

    await message.reply(await _convert_currency(quantity, currency_code, '/', db))


async def convert_to_rubles(message: Message, db: Database):
    try:
        quantity, currency_code = message.get_args().split()
    except ValueError:
        await message.reply("/to quantity currency [USD, EUR, etc.]")
        return

    await message.reply(await _convert_currency(quantity, currency_code, '*', db))


def register_user(dp: Dispatcher):
    dp.register_message_handler(
        user_start, CommandStart(), state="*"
    )

    dp.register_inline_handler(
        inline_handler, state="*", is_user=True,
    )

    dp.register_message_handler(
        convert_from_rubles, commands=["from"], state="*", is_user=True,
    )

    dp.register_message_handler(
        convert_to_rubles, commands=["to"], state="*", is_user=True,
    )
