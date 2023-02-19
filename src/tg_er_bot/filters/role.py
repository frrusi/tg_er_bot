import typing

from aiogram.dispatcher.filters import BoundFilter
from aiogram.dispatcher.handler import ctx_data
from aiogram.types.base import TelegramObject


class UserFilter(BoundFilter):
    key = "is_user"

    def __init__(self, is_user: typing.Optional[bool] = None):
        self.is_user = is_user

    async def check(self, obj: TelegramObject):
        data = ctx_data.get()
        return await data.get("db").get_user_role(obj["from"]["id"], "id")


class AdminFilter(BoundFilter):
    key = "is_admin"

    def __init__(self, is_admin: typing.Optional[bool] = None):
        self.is_admin = is_admin

    async def check(self, obj: TelegramObject):
        data = ctx_data.get()
        return await data.get("db").get_user_role(obj["from"]["id"], "is_admin")


class CreatorFilter(BoundFilter):
    key = "is_creator"

    def __init__(self, is_creator: typing.Optional[bool] = None):
        self.is_creator = is_creator

    async def check(self, obj: TelegramObject):
        data = ctx_data.get()
        return await data.get("db").get_user_role(obj["from"]["id"], "is_creator")
