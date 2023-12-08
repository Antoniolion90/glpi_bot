import glpi_api
from aiogram.types import Message

from bot.keyboards.inline import get_ticket_info_markup, get_type_ticket_markup, get_type_profiles_markup
from bot.states import AddTicket
from data import config
from loader import dp
from models import User

@dp.message_handler(i18n_text='Заявки 🆕')
async def _menu_spisok_ticket(message: Message, user: User):
    try:
        with glpi_api.connect(url=config.URL_GLPI, apptoken=config.APPTOKEN_GLPI, auth=user.token_user) as glpi:

            spisok = glpi.get_all_items('Ticket')

            await message.answer('Ваши заявки: ', reply_markup=get_ticket_info_markup(spisok))

    except glpi_api.GLPIError as err:
        await message.answer(str(err))

@dp.message_handler(i18n_text='Создать заявку ➕')
async def _menu_glpi_ticket(message: Message):

    await AddTicket.AT1.set()
    await message.answer('Выберите тип заявки:', reply_markup=get_type_ticket_markup())

@dp.message_handler(i18n_text='Мой профиль 👨‍💼')
async def _menu_glpi_profile(message: Message, user: User):
    try:
        with glpi_api.connect(url=config.URL_GLPI, apptoken=config.APPTOKEN_GLPI, auth=user.token_user) as glpi:

            profile = glpi.get_active_profile()

            await message.answer(f'Ваш профиль: #{profile["id"]} {profile["name"]}', reply_markup=get_type_profiles_markup())

    except glpi_api.GLPIError as err:
        await message.answer(str(err))