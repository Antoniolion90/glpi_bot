from aiogram.dispatcher.filters.state import StatesGroup, State


class AddTicket(StatesGroup):
    AT1 = State()  # принять название заявки
    AT2 = State()  # опишите свою проблему
    AT3 = State()  # выберите тип заявки
    AT4 = State()  # выберите срочность