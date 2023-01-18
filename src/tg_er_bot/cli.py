import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.files import JSONStorage
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from sqlalchemy import create_engine

from tg_er_bot.config import load_config
from tg_er_bot.filters.role import RoleFilter, AdminFilter
from tg_er_bot.handlers.admin import register_admin
from tg_er_bot.handlers.user import register_user
from tg_er_bot.middlewares.database import DatabaseMiddleware
from tg_er_bot.middlewares.role import RoleMiddleware
from tg_er_bot.utils.set_bot_commands import set_default_commands
from tg_er_bot.utils.startup_notify import on_startup_notify

logger = logging.getLogger(__name__)


def on_startup(dispatcher):
    set_default_commands(dispatcher)
    on_startup_notify(dispatcher)


def create_pool(user, password, database, host, port):
    return create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}")


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.error("Starting bot")
    config = load_config("../../bot.ini")

    if config.tg_bot.use_json:
        storage = JSONStorage(path="storage.json")
    else:
        storage = MemoryStorage()

    pool = create_pool(
        user=config.database.user,
        password=config.database.password,
        database=config.database.database,
        host=config.database.host,
        port=config.database.port
    )

    bot = Bot(token=config.tg_bot.token, parse_mode=types.ParseMode.HTML)
    dp = Dispatcher(bot, storage=storage)
    dp.middleware.setup(DatabaseMiddleware(pool))
    dp.middleware.setup(RoleMiddleware(config.tg_bot.admin_id))
    dp.filters_factory.bind(RoleFilter)
    dp.filters_factory.bind(AdminFilter)

    register_admin(dp)
    register_user(dp)

    # start
    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


def cli():
    """Wrapper for command line"""
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")


if __name__ == '__main__':
    cli()
