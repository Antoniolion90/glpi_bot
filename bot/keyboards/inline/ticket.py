from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_ticket_info_markup(spisok):
    markup = InlineKeyboardMarkup()
    for list in spisok:
        markup.add(InlineKeyboardButton(f'#{list["id"]}. {list["name"]}', callback_data=f'ticket_{list["id"]}'))
    return markup

def get_type_ticket_markup():
    type_ticket = InlineKeyboardMarkup()

    type_ticket.add(InlineKeyboardButton('Инцидент', callback_data='type_1'))
    type_ticket.add(InlineKeyboardButton('Запрос', callback_data='type_2'))

    return type_ticket

def get_urgency_ticket_markup():
    urgency_ticket = InlineKeyboardMarkup()

    urgency_ticket.add(InlineKeyboardButton('Очень низкая', callback_data='urgency_1'))
    urgency_ticket.add(InlineKeyboardButton('Низкая', callback_data='urgency_2'))
    urgency_ticket.add(InlineKeyboardButton('Средний', callback_data='urgency_3'))
    urgency_ticket.add(InlineKeyboardButton('Высокая', callback_data='urgency_4'))
    urgency_ticket.add(InlineKeyboardButton('Очень высокая', callback_data='urgency_5'))

    return urgency_ticket