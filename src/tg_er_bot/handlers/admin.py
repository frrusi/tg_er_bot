from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.utils.callback_data import CallbackData

from tg_er_bot.services.database import Database
from tg_er_bot.states.admin import BlockUser

start_keyboard_callback = CallbackData("start", "action")


def get_keyboard(buttons: tuple):
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard


async def update_text(message: Message, text: str):
    await message.edit_text(text)


async def admin_start(message: Message):
    buttons = (
        InlineKeyboardButton(text="Блокировка пользователя",
                             callback_data=start_keyboard_callback.new(action="block_user")),
    )

    await message.reply("Доступные действия:", reply_markup=get_keyboard(buttons))
    await BlockUser.menu.set()


async def get_user_id(call: CallbackQuery):
    await update_text(call.message, "Введите ID пользователя:")
    await call.answer()
    await BlockUser.id.set()


async def get_user_rights(message: Message, db: Database, state: FSMContext):
    if not await db.is_user_exists(message.text):
        await message.reply("Пользователь не найден")
        await BlockUser.menu.set()
        return

    await state.update_data({"id": message.text})

    buttons = (
        InlineKeyboardButton(text="Выдать", callback_data="give"),
        InlineKeyboardButton(text="Убрать", callback_data="remove")
    )

    await message.reply("Выберите тип запроса:", reply_markup=get_keyboard(buttons))
    await BlockUser.type.set()


async def set_user_rights(call: CallbackQuery, db: Database, state: FSMContext):
    user_data = await state.get_data()
    await db.set_rights("User", user_data["id"], "is_blocked", call.data == "give")
    await update_text(call.message, "success")
    await state.finish()


def register_admin(dp: Dispatcher):
    dp.register_message_handler(
        admin_start, commands=["admin"], state="*", is_admin=True,
    )

    dp.register_callback_query_handler(
        get_user_id, start_keyboard_callback.filter(action="block_user"), state=BlockUser.menu, is_admin=True,
    )

    dp.register_message_handler(
        get_user_rights, state=BlockUser.id, is_admin=True,
    )

    dp.register_callback_query_handler(
        set_user_rights, state=BlockUser.type, is_admin=True,
    )
