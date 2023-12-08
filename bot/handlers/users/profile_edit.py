import glpi_api
from aiogram.dispatcher.filters import Regexp
from aiogram.types import CallbackQuery

from bot.keyboards.inline import get_type_profiles_edit
from data import config
from loader import dp
from models import User


@dp.callback_query_handler(Regexp('profiles'))
async def _menu_number_profile(callback_query: CallbackQuery, user: User):
    await callback_query.message.edit_reply_markup(reply_markup=None)

    try:
        with glpi_api.connect(url=config.URL_GLPI, apptoken=config.APPTOKEN_GLPI, auth=user.token_user) as glpi:

            profiles = glpi.get_my_profiles()

            await callback_query.message.answer(f'Ваши профили:', reply_markup=get_type_profiles_edit(profiles))

    except glpi_api.GLPIError as err:
        await callback_query.message.answer(str(err))

@dp.callback_query_handler(Regexp('profile_'))
async def _menu_number_edit_profile(callback_query: CallbackQuery, user: User):
    await callback_query.message.edit_reply_markup(reply_markup=None)
    id_profile = callback_query.data[8:]

    try:
        with glpi_api.connect(url=config.URL_GLPI, apptoken=config.APPTOKEN_GLPI, auth=user.token_user) as glpi:

            glpi.set_active_profile(id_profile)

            await callback_query.message.answer(f'Ваш профиль изменен на {glpi.get_active_profile()["name"]}')

    except glpi_api.GLPIError as err:
        await callback_query.message.answer(str(err))