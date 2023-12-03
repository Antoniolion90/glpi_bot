from aiogram.dispatcher.filters.state import StatesGroup, State


class AddToken(StatesGroup):
    AP1 = State()  # принять токен пользователя
