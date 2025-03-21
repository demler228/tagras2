from aiogram.utils.keyboard import InlineKeyboardBuilder

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
        text="Удалить мероприятие",
        callback_data='delete_event'
    )

    builder.button(
        text="🔙 Назад",
        callback_data=''
    )
    builder.adjust(3,1)
    return builder.as_markup()

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
        callback_data='office_maps_button_admin'
    )
    builder.adjust(1)
    return builder.as_markup()
