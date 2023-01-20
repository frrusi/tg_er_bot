from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import Message

from tg_er_bot.services.database import Database


async def user_start(message: Message, db: Database, state: FSMContext):
    await state.reset_state()
    await db.add_user(**message.from_user.values)
    await message.reply(f"Привет, {message.from_user.first_name}!")


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, CommandStart(), state="*")
