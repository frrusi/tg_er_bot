from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.utils.callback_data import CallbackData
from prettytable import PrettyTable

from tg_er_bot.services.database import Database
from tg_er_bot.states.creator import SetAdmin

start_keyboard_callback = CallbackData("start", "action")


def get_keyboard(buttons: tuple):
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard


async def update_text(message: Message, text: str):
    await message.edit_text(text)


async def creator_start(message: Message):
    buttons = (
        InlineKeyboardButton(text="Список администраторов",
                             callback_data=start_keyboard_callback.new(action="get_admins")),
        InlineKeyboardButton(text="Выдать права администратора",
                             callback_data=start_keyboard_callback.new(action="set_admin"))
    )

    await message.reply("Доступные действия:", reply_markup=get_keyboard(buttons))
    await SetAdmin.menu.set()


async def get_list_admins(call: CallbackQuery, db: Database, state: FSMContext):
    table = PrettyTable(field_names=(admins := await db.get_admins()).keys())
    table.add_rows(admins)

    await update_text(call.message, "Вывожу список администраторов..")
    await call.message.answer(f"\n<pre>{table}</pre>")
    await call.answer()
    await state.finish()


async def get_admin_id(call: CallbackQuery):
    await update_text(call.message, "Введите ID пользователя:")
    await call.answer()
    await SetAdmin.id.set()


async def get_admin_rights(message: Message, db: Database, state: FSMContext):
    if not await db.is_user_exists(message.text):
        await message.reply("Пользователь не найден")
        await SetAdmin.menu.set()
        return

    await state.update_data({"id": message.text})

    buttons = (
        InlineKeyboardButton(text="Выдать", callback_data="give"),
        InlineKeyboardButton(text="Забрать", callback_data="remove")
    )

    await message.reply("Выберите тип запроса:", reply_markup=get_keyboard(buttons))
    await SetAdmin.type.set()


async def set_admin_rights(call: CallbackQuery, db: Database, state: FSMContext):
    user_data = await state.get_data()
    await db.set_rights("User", user_data["id"], "is_admin", call.data == "give")
    await update_text(call.message, "success")
    await state.finish()


def register_creator(dp: Dispatcher):
    dp.register_message_handler(
        creator_start, commands=["creator"], state="*", is_creator=True,
    )

    dp.register_callback_query_handler(
        get_list_admins, start_keyboard_callback.filter(action="get_admins"), state=SetAdmin.menu, is_creator=True,
    )

    dp.register_callback_query_handler(
        get_admin_id, start_keyboard_callback.filter(action="set_admin"), state=SetAdmin.menu, is_creator=True,
    )

    dp.register_message_handler(
        get_admin_rights, state=SetAdmin.id, is_creator=True,
    )

    dp.register_callback_query_handler(
        set_admin_rights, state=SetAdmin.type, is_creator=True,
    )
