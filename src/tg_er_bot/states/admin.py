from aiogram.dispatcher.filters.state import StatesGroup, State


class BlockUser(StatesGroup):
    menu = State()
    id = State()
    type = State()
