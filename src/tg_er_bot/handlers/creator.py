from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, ReplyKeyboardMarkup
from prettytable import PrettyTable
from sqlalchemy import true

from tg_er_bot.services.database import Database
from tg_er_bot.states.creator import SetAdmin


async def creator_start(message: Message):
    creator_menu_buttons = ["Список администраторов", "Выдать права администратора"]
    creator_menu_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(*creator_menu_buttons)

    await message.reply("Выберите действие", reply_markup=creator_menu_keyboard)
    await SetAdmin.menu.set()


async def get_list_admins(message: Message, db: Database):
    table = PrettyTable(field_names=(admins := await db.get_admins()).keys())
    table.add_rows(admins)
    await message.reply(f"<pre>{table}</pre>")


async def get_admin_id(message: Message):
    await message.reply("Введите ID пользователя:")
    await SetAdmin.id.set()


async def get_admin_rights(message: Message, db: Database, state: FSMContext):
    if not await db.is_user_exists(message.text):
        await message.reply("Пользователь не найден")
        await SetAdmin.menu.set()

    await state.update_data({"id": message.text})

    set_admin_rights_buttons = ["Добавить", "Удалить"]
    set_admin_rights_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(*set_admin_rights_buttons)
    await message.reply("Выберите тип запроса:", reply_markup=set_admin_rights_menu)
    await SetAdmin.type.set()

async def set_admin_rights(message: Message, db: Database, state: FSMContext):
    user_data = await state.get_data()

    if message.text == "Добавить":
        await db.set_rights("User", user_data["id"], "is_admin", True)
        await message.reply('Админ добавлен')

    await state.finish()


def register_creator(dp: Dispatcher):
    dp.register_message_handler(
        creator_start, commands=["creator"], state="*", is_creator=True,
    )

    dp.register_message_handler(
        get_list_admins, Text(equals="Список администраторов"), state=SetAdmin.menu, is_creator=True,
    )

    dp.register_message_handler(
        get_admin_id, Text(equals="Выдать права администратора"), state=SetAdmin.menu, is_creator=True,
    )

    dp.register_message_handler(
        get_admin_rights, state=SetAdmin.id, is_creator=True,
    )

    dp.register_message_handler(
        set_admin_rights, state=SetAdmin.type, is_creator=True,
    )