from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder

class BackToEventMenuCallback(CallbackData, prefix="back_to_event_menu"):
    event_id: int

def get_event_menu_keyboard(event_id: int):
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Изменить название",
        callback_data='change_event_name'
    )
    builder.button(
        text="Изменить описание",
        callback_data='change_event_description'
    )
    builder.button(
        text="Изменить дату",
        callback_data='change_event_date'
    )
    builder.button(
        text="Удалить участника(ов)",
        callback_data='change_event_members'
    )
    builder.button(
        text="Удалить мероприятие",
        callback_data='delete_event'
    )
    builder.button(
        text="🔙 Назад",
        callback_data=BackToEventMenuCallback(event_id)
    )
    builder.adjust(1)
    return builder.as_markup()