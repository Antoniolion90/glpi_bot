import glpi_api
from aiogram.types import Message
from loader import dp


@dp.message_handler(i18n_text='menu')
async def _menu_glpi(message: Message):

    URL = 'https://help.uzairports.com//apirest.php'
    APPTOKEN = '9ZumD7bMJeXrU0aF8V9UVrMobsSwcvqn26e4diPn'
    USERTOKEN = '6oussx3qkS6ILN77fOmp9ZtC7sWrSXGcCxlmlV3R'
    try:
        with glpi_api.connect(url=URL, apptoken=APPTOKEN, auth=('a.postnikov', 'Nokia0910033@')) as glpi:
            print(glpi.add('Ticket',
                     {'type': 2, 'urgency': 5, 'name': 'Тестовая заявка', 'content': 'Тест примерно'}))

    except glpi_api.GLPIError as err:
        print(str(err))

    await message.answer('привет')