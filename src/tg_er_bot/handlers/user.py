from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from tg_er_bot.services.database import Database


async def user_start(message: Message, db: Database, state: FSMContext):
    await db.add_user(**message.from_user.values)
    await message.reply("Hello, user!")
    # await state.set_state(User.SOME_STATE)


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
