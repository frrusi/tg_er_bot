import emoji
from aiogram import Dispatcher
from aiogram.types import Message
from prettytable import PrettyTable

from tg_er_bot.services.database import Database


async def get_list_admins(message: Message, db: Database):
    table = PrettyTable(field_names=("ID", "Username"))

    if not (admins := (await db.get_admins())):
        await message.reply("Админы не найдены")
        return

    table.add_rows(admins)

    await message.reply("Вывожу список администраторов..")
    await message.answer(f"\n<pre>{table}</pre>")


async def set_admin_rights(message: Message, db: Database):
    try:
        user_id, request_type = message.get_args().split()
    except ValueError:
        await message.reply("/set_admin user_id [true / false]")
        return

    await db.set_rights(user_id, "is_admin", request_type.lower() == "true")
    await message.reply(emoji.emojize(":check_mark_button:"))


def register_creator(dp: Dispatcher):
    dp.register_message_handler(
        get_list_admins, commands=["get_admins"], state="*", is_creator=True,
    )

    dp.register_message_handler(
        set_admin_rights, commands=["set_admin"], state="*", is_creator=True,
    )
