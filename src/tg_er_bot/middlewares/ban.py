from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Message, CallbackQuery, InlineQuery


class UserBannedMiddleware(BaseMiddleware):
    @staticmethod
    async def on_process_message(message: Message, data: dict):
        is_blocked = await data["db"].is_user_blocked(message.from_user.id)

        if is_blocked:
            await message.answer("<b>Аккаунт заблокирован</b>")
            raise CancelHandler

    @staticmethod
    async def on_process_callback_query(call: CallbackQuery, data: dict):
        is_blocked = await data["db"].is_user_blocked(call.from_user.id)

        if is_blocked:
            await call.answer("Аккаунт заблокирован", show_alert=True)
            raise CancelHandler

    @staticmethod
    async def on_process_inline_query(query: InlineQuery, data: dict):
        is_blocked = await data["db"].is_user_blocked(query.from_user.id)

        if is_blocked:
            raise CancelHandler
