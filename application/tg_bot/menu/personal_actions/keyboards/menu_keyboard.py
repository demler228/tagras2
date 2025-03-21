from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder




def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="FAQ", callback_data="faq_button")
    builder.button(text="Полезные контакты", callback_data="contacts_button")
    builder.button(text="Мероприятия и встречи", callback_data="events_button")
    builder.button(text="Задачи", callback_data="tasks_button")
    builder.button(text="Мой профиль", callback_data="profile_button")
    builder.button(text="Карты офиса", callback_data="office_maps_button")
    builder.button(text="ИИ - Помощник", callback_data="ai_assistant_button")
    builder.button(text="Тренинги", callback_data="training_button")

    builder.adjust(1)

    return builder.as_markup()