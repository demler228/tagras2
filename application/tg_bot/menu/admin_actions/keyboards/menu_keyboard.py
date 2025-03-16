from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder




def get_admin_main_menu_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="FAQ", callback_data="faq_button_admin")
    builder.button(text="Тренинги", callback_data="training_button_admin")


    builder.adjust(1)

    return builder.as_markup()