from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_type_profiles_markup():
    type_profile = InlineKeyboardMarkup()
    type_profile.add(InlineKeyboardButton('Сменить профиль', callback_data='profiles'))
    return type_profile

def get_type_profiles_edit(profiles):
    edit_profile = InlineKeyboardMarkup()
    for prof in profiles:
        edit_profile.add(InlineKeyboardButton(f'#{prof["id"]} {prof["name"]}', callback_data=f'profile_{prof["id"]}'))
    return edit_profile