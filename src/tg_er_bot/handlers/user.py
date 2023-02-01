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
            message_text="message_text"
        )
    ) for currency in currencies]

    await query.answer(articles, cache_time=60, is_personal=True)


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, CommandStart(), state="*")

    dp.register_inline_handler(inline_handler, state="*")
