from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware

from tg_er_bot.services.database import Database


class DatabaseMiddleware(LifetimeControllerMiddleware):
    skip_patterns = ["error", "update"]

    def __init__(self, pool):
        super().__init__()
        self.pool = pool

    async def pre_process(self, obj, data, *args):
        data["db"] = Database(self.pool)

    async def post_process(self, obj, data, *args):
        del data["db"]
