import math

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from loader import _

def pag_ticket():
    pag_ticket = CallbackData("ticket", "action", "page")
    return pag_ticket


def get_ticket_info_markup(tickets, page: int = 0):

    count = int(len(tickets))
    max_list = 5

    markup = InlineKeyboardMarkup()

    if page == 0:
        for flight in tickets[page:max_list]:
            markup.add(depart_tickets_list(flight))
        if count > 5:
            markup.row(InlineKeyboardButton(f'📖 {page + 1}/{math.ceil(count / max_list)}', callback_data='pust'),
                       InlineKeyboardButton(_('⏭ След.'), callback_data=pag_ticket().new(action='next', page=page)))

    elif page == math.ceil((count / max_list) - 1):
        for flight in tickets[(max_list * page):(page * max_list + max_list)]:
            markup.add(depart_tickets_list(flight))

        markup.row(InlineKeyboardButton(_('⏮ Пред.'), callback_data=pag_ticket().new(action='prev', page=page)),
                   InlineKeyboardButton(f'📖 {page + 1}/{math.ceil(count / max_list)}', callback_data='pust'))

    else:
        for flight in tickets[(max_list * page):(page * max_list + max_list)]:
            markup.add(depart_tickets_list(flight))

        markup.row(InlineKeyboardButton(_('⏮ Пред.'), callback_data=pag_ticket().new(action='prev', page=page)),
                   InlineKeyboardButton(f'📖 {page + 1}/{math.ceil(count / max_list)}', callback_data='pust'),
                   InlineKeyboardButton(_('⏭ След.'), callback_data=pag_ticket().new(action='next', page=page)))
    return markup

def depart_tickets_list(list):
    return InlineKeyboardButton(f'#{list["id"]}. {list["name"]}', callback_data=f'ticket_{list["id"]}')

def get_type_ticket_markup():
    type_ticket = InlineKeyboardMarkup()

    type_ticket.add(InlineKeyboardButton(_('Инцидент'), callback_data='type_1'))
    type_ticket.add(InlineKeyboardButton(_('Запрос'), callback_data='type_2'))

    return type_ticket


def get_urgency_ticket_markup():
    urgency_ticket = InlineKeyboardMarkup()

    urgency_ticket.add(InlineKeyboardButton(_('Очень низкая'), callback_data='urgency_1'))
    urgency_ticket.add(InlineKeyboardButton(_('Низкая'), callback_data='urgency_2'))
    urgency_ticket.add(InlineKeyboardButton(_('Средний'), callback_data='urgency_3'))
    urgency_ticket.add(InlineKeyboardButton(_('Высокая'), callback_data='urgency_4'))
    urgency_ticket.add(InlineKeyboardButton(_('Очень высокая'), callback_data='urgency_5'))

    return urgency_ticket
