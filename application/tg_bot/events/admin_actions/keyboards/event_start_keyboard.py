from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_event_start_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Добавить мероприятие",
        callback_data='create_event'
    )
    builder.button(
        text="Просмотреть мероприятия",
        callback_data='view_events'
    )
    builder.button(
        text="🔙 Назад в меню",
        callback_data='back_to_admin_main_menu'
    )
    builder.adjust(1)
    return builder.as_markup()
