import glpi_api
from aiogram.dispatcher.filters import Regexp
from aiogram.types import CallbackQuery

from bot.keyboards.default import get_default_glpi_token
from bot.keyboards.inline import get_type_profiles_edit
from data import config
from loader import dp, _
from models import User


@dp.callback_query_handler(Regexp('profiles'))
async def _menu_number_profile(callback_query: CallbackQuery, user: User):
    await callback_query.message.edit_reply_markup(reply_markup=None)

    try:
        with glpi_api.connect(url=config.URL_GLPI, apptoken=config.APPTOKEN_GLPI, auth=user.token_user) as glpi:

            profiles = glpi.get_my_profiles()
            await callback_query.message.answer(_('Ваши профили:'), reply_markup=get_type_profiles_edit(profiles))

    except glpi_api.GLPIError as err:
        oshibka = str(err).split(' ')
        if oshibka[0] == '(ERROR_GLPI_LOGIN_USER_TOKEN)':
            await callback_query.message.answer(_('Ошибка. Необходимо авторизоваться! 👇'), reply_markup=get_default_glpi_token())
        else:
            await callback_query.message.answer(str(err))
    except Exception:
        await callback_query.message.answer(_('Неправильный токен. Пройдите авторизацию повторно'), reply_markup=get_default_glpi_token())

@dp.callback_query_handler(Regexp('profile_'))
async def _menu_number_edit_profile(callback_query: CallbackQuery, user: User):
    await callback_query.message.edit_reply_markup(reply_markup=None)
    id_profile = callback_query.data[8:]

    try:
        with glpi_api.connect(url=config.URL_GLPI, apptoken=config.APPTOKEN_GLPI, auth=user.token_user) as glpi:

            glpi.set_active_profile(id_profile)

            query = User.update(glpi_profile_id=glpi.get_active_profile()["id"]).where(User.id == user.id)
            query.execute()

            await callback_query.message.answer(_('Ваш профиль изменен на {name}')).format(name=glpi.get_active_profile()["name"])

    except glpi_api.GLPIError as err:
        await callback_query.message.answer(str(err))