from aiogram.utils.keyboard import InlineKeyboardBuilder

from application.tg_bot.events.admin_actions.keyboards.callbacks import BackToEventMenuCallback


def get_event_menu_keyboard(event_id: int,callback):
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
        callback_data=callback
    )
    builder.adjust(1)
    return builder.as_markup()