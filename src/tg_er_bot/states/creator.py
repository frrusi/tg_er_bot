from aiogram.dispatcher.filters.state import StatesGroup, State


class SetAdmin(StatesGroup):
    menu = State()
    id = State()
    type = State()
