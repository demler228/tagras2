from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder




def get_admin_main_menu_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="FAQ", callback_data="faq_button_admin")
    builder.button(text="Полезные контакты", callback_data="contacts_button")
    builder.button(text="Мой профиль", callback_data="profile_button")
    builder.button(text="Карты офиса", callback_data="office_maps_button")
    builder.button(text="ИИ - Помощник", callback_data="ai_assistant_button")

    builder.adjust(1)

    return builder.as_markup()