import glpi_api
from aiogram.dispatcher.filters import Regexp
from aiogram.types import Message, CallbackQuery

from bot.keyboards.inline import get_ticket_info_markup
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

@dp.callback_query_handler(Regexp('ticket_'))
async def _menu_number_ticket(callback_query: CallbackQuery, user: User):
    code = callback_query.data[7:]

    await callback_query.message.edit_reply_markup(reply_markup=None)

    try:
        with glpi_api.connect(url=config.URL_GLPI, apptoken=config.APPTOKEN_GLPI, auth=user.token_user) as glpi:

            spisok = glpi.get_item('Ticket', code)

            text = f'#{spisok["id"]}. Название: {spisok["name"]} \nОписание: {spisok["content"]} \nДата открытия: {spisok["date"]}'

    except glpi_api.GLPIError as err:
        text = str(err)

    await callback_query.message.answer(text)
