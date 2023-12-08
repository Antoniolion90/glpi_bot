import glpi_api
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Regexp
from aiogram.types import Message, CallbackQuery

from bot.keyboards.default import get_default_glpi_token
from bot.keyboards.inline import get_urgency_ticket_markup
from bot.states import AddTicket
from data import config
from loader import dp, _
from models import User

@dp.callback_query_handler(Regexp('type_'), state=AddTicket.AT1)
async def _change_glpi_ticket_type(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.edit_reply_markup(reply_markup=None)

    ticket_type = callback_query.data[5:]

    async with state.proxy() as data:
        data['answer1'] = ticket_type

    await callback_query.message.answer(_('Выберите срочность:'), reply_markup=get_urgency_ticket_markup())
    await AddTicket.next()

@dp.callback_query_handler(Regexp('urgency_'), state=AddTicket.AT2)
async def _change_glpi_urgency_ticket(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.edit_reply_markup(reply_markup=None)

    ticket_urgency = callback_query.data[8:]

    await state.update_data(answer2=ticket_urgency)
    await callback_query.message.answer(_('Напишите название заявки:'))
    await AddTicket.next()

@dp.message_handler(state=AddTicket.AT3)
async def _default_name_ticket(message: Message, state: FSMContext):
    ticket_name = message.text

    await state.update_data(answer3=ticket_name)

    await message.answer(_('Опишите свою проблему:'))
    await AddTicket.next()

@dp.message_handler(state=AddTicket.AT4)
async def _default_content_ticket(message: Message, state: FSMContext, user: User):
    ticket_content = message.text

    data = await state.get_data()
    ticket_type = data.get('answer1')
    ticket_urgency = data.get('answer2')
    ticket_name = data.get('answer3')

    try:
        with glpi_api.connect(url=config.URL_GLPI, apptoken=config.APPTOKEN_GLPI, auth=user.token_user) as glpi:
            profile = glpi.get_full_session()
            mess = glpi.add('Ticket', {'_users_id_requester': profile['glpiID'], 'type': ticket_type, 'urgency': ticket_urgency, 'requesttypes_id': 8, 'name': ticket_name, 'content': ticket_content})
            text = str(mess[0]['message'])

            await message.answer(text)

    except glpi_api.GLPIError as err:
        oshibka = str(err).split(' ')

        if oshibka[0] == '(ERROR_GLPI_LOGIN_USER_TOKEN)':
            await message.answer(_('Ошибка. Необходимо авторизоваться! 👇'), reply_markup=get_default_glpi_token())
        else:
            await message.answer(str(err))
    except Exception:
        await message.answer(_('Неправильный токен. Пройдите авторизацию повторно'), reply_markup=get_default_glpi_token())

    await state.finish()