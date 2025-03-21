from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_event_menu_keyboard():
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
        text="Изменить участников",
        callback_data='change_event_users'
    )
    builder.button(
        text="Удалить мероприятие",
        callback_data='delete_event'
    )
    builder.button(
        text="🔙 Назад",
        callback_data='events_button_admin'
    )
    builder.adjust(1)
    return builder.as_markup()