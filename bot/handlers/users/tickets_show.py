import glpi_api
from aiogram.dispatcher.filters import Regexp
from aiogram.types import CallbackQuery

from bot.keyboards.inline import pag_ticket, get_ticket_info_markup
from data import config
from loader import dp, _
from models import User


@dp.callback_query_handler(pag_ticket().filter(action='prev'))
async def _prev_page_ticket(callback_query: CallbackQuery, callback_data: dict, user: User):
    page = int(callback_data['page']) - 1

    try:
        with glpi_api.connect(url=config.URL_GLPI, apptoken=config.APPTOKEN_GLPI, auth=user.token_user) as glpi:

            spisok = glpi.get_all_items('Ticket')
            await callback_query.message.edit_reply_markup(reply_markup=get_ticket_info_markup(spisok, page))

    except glpi_api.GLPIError as err:
        await callback_query.message.answer(str(err))


@dp.callback_query_handler(pag_ticket().filter(action='next'))
async def _next_page_ticket(callback_query: CallbackQuery, callback_data: dict, user: User):
    page = int(callback_data['page']) + 1

    try:
        with glpi_api.connect(url=config.URL_GLPI, apptoken=config.APPTOKEN_GLPI, auth=user.token_user) as glpi:

            spisok = glpi.get_all_items('Ticket')
            await callback_query.message.edit_reply_markup(reply_markup=get_ticket_info_markup(spisok, page))

    except glpi_api.GLPIError as err:
        await callback_query.message.answer(str(err))


@dp.callback_query_handler(Regexp('ticket_'))
async def _menu_number_ticket(callback_query: CallbackQuery, user: User):
    code = callback_query.data[7:]

    await callback_query.message.edit_reply_markup(reply_markup=None)

    try:
        with glpi_api.connect(url=config.URL_GLPI, apptoken=config.APPTOKEN_GLPI, auth=user.token_user) as glpi:

            spisok = glpi.get_item('Ticket', code)

            criteria = [{'field': 2, 'searchtype': 'contains', 'value': code}]
            forcedisplay = [1, 5, 27]  # name, specialist
            specialist_id = glpi.search('Ticket', criteria=criteria, forcedisplay=forcedisplay)

            if (specialist_id[0]["5"] == None):
                specialist_name = _('не назначен')
            else:
                specialist_name = _('назначен (#{specialist})').format(specialist=specialist_id[0]["5"])

            text = _('#{id}. Название заявки: {name} \n'
                     'Описание: {content} \n'
                     'Дата открытия: {date} \n'
                     'Назначенный специалист: {specialist} \n'
                     'Статус заявки: {status}\n'
                     'Кол-во комментарий: {comment}').format(id=spisok["id"], name=spisok["name"], content=spisok["content"], date=spisok["date"], specialist=specialist_name, status=config.STATUS_GLPI[spisok["status"]], comment=specialist_id[0]["27"])

    except glpi_api.GLPIError as err:
        text = str(err)

    await callback_query.message.answer(text)
