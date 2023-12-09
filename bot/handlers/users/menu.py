import glpi_api
from aiogram.types import Message

from bot.keyboards.default import get_default_glpi_token
from bot.keyboards.inline import get_ticket_info_markup, get_type_ticket_markup, get_type_profiles_markup
from bot.states import AddTicket
from data import config
from loader import dp, _
from models import User

@dp.message_handler(i18n_text='Заявки 🆕')
async def _menu_spisok_ticket(message: Message, user: User):
    try:
        with glpi_api.connect(url=config.URL_GLPI, apptoken=config.APPTOKEN_GLPI, auth=user.token_user) as glpi:
            glpi.set_active_profile(user.glpi_profile_id)

            spisok = glpi.get_all_items('Ticket')

            await message.answer(_('Ваши заявки:'), reply_markup=get_ticket_info_markup(spisok))

    except glpi_api.GLPIError as err:
        oshibka = str(err).split(' ')

        if oshibka[0] == '(ERROR_GLPI_LOGIN_USER_TOKEN)':
            await message.answer(_('Ошибка. Необходимо авторизоваться! 👇'), reply_markup=get_default_glpi_token())
        else:
            await message.answer(str(err))
    except Exception:
        await message.answer(_('Неправильный токен. Пройдите авторизацию повторно'), reply_markup=get_default_glpi_token())


@dp.message_handler(i18n_text='Создать заявку ➕')
async def _menu_glpi_ticket(message: Message):

    await AddTicket.AT1.set()
    await message.answer(_('Выберите тип заявки:'), reply_markup=get_type_ticket_markup())

@dp.message_handler(i18n_text='Мой профиль 👨‍💼')
async def _menu_glpi_profile(message: Message, user: User):
    try:
        with glpi_api.connect(url=config.URL_GLPI, apptoken=config.APPTOKEN_GLPI, auth=user.token_user) as glpi:

            profile = glpi.get_my_profiles()

            for prof in profile:
                if prof["id"] == user.glpi_profile_id:
                    await message.answer(_('Ваш профиль: #{id} {name}').format(id=prof["id"], name=prof["name"]), reply_markup=get_type_profiles_markup())


    except glpi_api.GLPIError as err:
        oshibka = str(err).split(' ')
        if oshibka[0] == '(ERROR_GLPI_LOGIN_USER_TOKEN)':
            await message.answer(_('Ошибка. Необходимо авторизоваться! 👇'), reply_markup=get_default_glpi_token())
        else:
            await message.answer(str(err))
    except Exception:
        await message.answer(_('Неправильный токен. Пройдите авторизацию повторно'), reply_markup=get_default_glpi_token())