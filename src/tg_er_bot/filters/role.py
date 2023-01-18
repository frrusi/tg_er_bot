import typing

from aiogram.dispatcher.filters import BoundFilter
from aiogram.dispatcher.handler import ctx_data
from aiogram.types.base import TelegramObject

from tg_er_bot.models.role import UserRole


class RoleFilter(BoundFilter):
    key = 'role'

    def __init__(
            self,
            role: typing.Union[None, UserRole, typing.Collection[UserRole]] = None,
    ):
        if role is None:
            self.roles = None
        elif isinstance(role, UserRole):
            self.roles = {role}
        else:
            self.roles = set(role)

    async def check(self, obj: TelegramObject):
        if self.roles is None:
            return True
        data = ctx_data.get()
        return data.get("role") in self.roles


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
