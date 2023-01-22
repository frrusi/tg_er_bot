from aiogram import Dispatcher
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.utils.callback_data import CallbackData
from prettytable import PrettyTable

from tg_er_bot.services.database import Database
from tg_er_bot.states.creator import SetAdmin

start_keyboard = CallbackData("start", "func")
back_button = CallbackData("back", "func")


def get_start_keyboard():
    buttons = (
        InlineKeyboardButton(text="Список администраторов", callback_data=start_keyboard.new(func="get_list_admins")),
        InlineKeyboardButton(text="Выдать права администратора", callback_data=start_keyboard.new(func="num_incr"))
    )

    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    return keyboard


# async def update_text(message: Message, new_value: int):
#     await message.edit_text(f"Укажите число: {new_value}", reply_markup=get_keyboard())


async def creator_start(message: Message):
    await message.reply("Доступные действия:", reply_markup=get_start_keyboard())
    await SetAdmin.menu.set()


async def get_list_admins(call: CallbackQuery, db: Database):  # TODO
    buttons = (
        InlineKeyboardButton(text="Назад", callback_data=back_button.new(func="get_list_admins")),
    )

    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)

    table = PrettyTable(field_names=(admins := await db.get_admins()).keys())
    table.add_rows(admins)

    await call.message.edit_text(f"Список администраторов:\n<pre>{table}</pre>", reply_markup=keyboard)
    await call.answer()


# async def get_admin_id(message: Message):
#     await message.reply("Введите ID пользователя:")
#     await SetAdmin.id.set()
#
#
# async def get_admin_rights(message: Message, db: Database, state: FSMContext):
#     if not await db.is_user_exists(message.text):
#         await message.reply("Пользователь не найден")
#         await SetAdmin.menu.set()
#
#     await state.update_data({"id": message.text})
#
#     set_admin_rights_buttons = ["Добавить", "Удалить"]
#     set_admin_rights_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(*set_admin_rights_buttons)
#     await message.reply("Выберите тип запроса:", reply_markup=set_admin_rights_menu)
#     await SetAdmin.type.set()
#
#
# async def set_admin_rights(message: Message, db: Database, state: FSMContext):
#     user_data = await state.get_data()
#
#     if message.text == "Добавить":
#         await db.set_rights("User", user_data["id"], "is_admin", True)
#         await message.reply('Админ добавлен')
#
#     await state.finish()


def register_creator(dp: Dispatcher):
    dp.register_message_handler(
        creator_start, commands=["creator"], state="*", is_creator=True,
    )

    dp.register_callback_query_handler(
        get_list_admins, start_keyboard.filter(func="get_list_admins"), state=SetAdmin.menu, is_creator=True,
    )

    # dp.register_message_handler(
    #     get_admin_id, Text(equals="Выдать права администратора"), state=SetAdmin.menu, is_creator=True,
    # )
    #
    # dp.register_message_handler(
    #     get_admin_rights, state=SetAdmin.id, is_creator=True,
    # )
    #
    # dp.register_message_handler(
    #     set_admin_rights, state=SetAdmin.type, is_creator=True,
    # )
