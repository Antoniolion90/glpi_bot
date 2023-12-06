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

            criteria = [{'field': 2, 'searchtype': 'contains', 'value': code}]
            forcedisplay = [1, 5]  # name, specialist
            specialist_id = glpi.search('Ticket', criteria=criteria, forcedisplay=forcedisplay)

            if (specialist_id[0]["5"] == None):
                specialist_name = 'не назначен'
            else:
                specialist_n = glpi.get_multiple_items({'itemtype': 'User', 'items_id': specialist_id[0]["5"]})
                specialist_name = str(specialist_n[0]["name"])

            text = f'#{spisok["id"]}. Название заявки: {spisok["name"]} \nОписание: {spisok["content"]} \nДата открытия: {spisok["date"]} \nНазначенный специалист: {specialist_name} \nСтатус заявки: {config.STATUS_GLPI[spisok["status"]]}'

    except glpi_api.GLPIError as err:
        text = str(err)

    await callback_query.message.answer(text)
