import emoji
from aiogram import Dispatcher
from aiogram.types import Message

from tg_er_bot.services.database import Database


async def set_ban_status(message: Message, db: Database):
    try:
        user_id, request_type = message.get_args().split()
    except ValueError:
        await message.reply("/ban user_id [true / false]")
        return

    await db.set_rights(user_id, "is_blocked", request_type == "true")
    await message.reply(emoji.emojize(":check_mark_button:"))


def register_admin(dp: Dispatcher):
    dp.register_message_handler(
        set_ban_status, commands=["ban"], state="*", is_admin=True,
    )
