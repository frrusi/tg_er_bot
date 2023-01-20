from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, ReplyKeyboardMarkup
from prettytable import PrettyTable

from tg_er_bot.services.database import Database


async def creator_start(message: Message):
    creator_menu_buttons = ["Список администраторов", "Выдать права администратора"]
    creator_menu_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(*creator_menu_buttons)

    await message.reply("Выберите действие", reply_markup=creator_menu_keyboard)


async def creator_get_admins(message: Message, db: Database):
    table = PrettyTable(field_names=["id", "username"])
    table.add_rows(await db.get_admins())
    await message.reply(f"<pre>{table}</pre>")


def register_creator(dp: Dispatcher):
    dp.register_message_handler(
        creator_start, commands=["creator"], state="*", is_creator=True,
    )

    dp.register_message_handler(
        creator_get_admins, Text(equals="Список администраторов"), state="*", is_creator=True,
    )
