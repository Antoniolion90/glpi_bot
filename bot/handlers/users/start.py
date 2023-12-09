import glpi_api
from aiogram.dispatcher.filters.builtin import CommandStart, CommandHelp
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from bot.commands import get_admin_commands, get_default_commands
from bot.commands import set_admin_commands
from bot.keyboards.default import get_default_markup, get_default_glpi_token
from bot.keyboards.inline import get_language_inline_markup

from bot.states import AddToken
from data import config
from loader import dp, _
from models import User


@dp.message_handler(CommandStart())
async def _start(message: Message, user: User):
    if user.is_admin:
        await set_admin_commands(user.id, user.language)

    text = _('Hi {full_name}!\n'
             'Choose your language').format(full_name=user.name)

    await message.answer(text, reply_markup=get_language_inline_markup())


@dp.message_handler(i18n_text='Вход в GLPI 🔐')
async def _start_token(message: Message, user: User):
    if user.is_admin:
        await set_admin_commands(user.id, user.language)

    text = _('Отправьте токен пользователя для авторизации в glpi')

    await AddToken.AP1.set()
    await message.answer(text)

@dp.message_handler(i18n_text='Выход из GLPI 🚪')
async def _start_token(message: Message, user: User):
    query = User.update(token_user=None, glpi_profile_id=None).where(User.id == user.id)
    query.execute()

    await message.answer(_('Вышли из GLPI'), reply_markup=get_default_glpi_token())

@dp.message_handler(state=AddToken.AP1)
async def _default_menu(message: Message, state: FSMContext, user: User):
    user_token = message.text
    try:
        with glpi_api.connect(url=config.URL_GLPI, apptoken=config.APPTOKEN_GLPI, auth=user_token) as glpi:

            glpi.get_active_profile()

            query = User.update(token_user=user_token, glpi_profile_id=glpi.get_active_profile()["id"]).where(User.id == message.from_id)
            query.execute()

        await message.answer(_('Успешно авторазовались'), reply_markup=get_default_markup(user))

    except glpi_api.GLPIError as err:
        oshibka = str(err).split(' ')

        if oshibka[0] == '(ERROR_GLPI_LOGIN_USER_TOKEN)':
            await message.answer(_('Ошибка. Необходимо авторизоваться! 👇'), reply_markup=get_default_glpi_token())
        else:
            await message.answer(str(err))
    except Exception:
        await message.answer(_('Неправильный токен. Пройдите авторизацию повторно'), reply_markup=get_default_glpi_token())

    await state.finish()


@dp.message_handler(i18n_text='Help 🆘')
@dp.message_handler(CommandHelp())
async def _help(message: Message, user: User):
    commands = get_admin_commands(user.language) if user.is_admin else get_default_commands(user.language)

    text = _('Help 🆘') + '\n\n'
    for command in commands:
        text += f'{command.command} - {command.description}\n'

    await message.answer(text)
