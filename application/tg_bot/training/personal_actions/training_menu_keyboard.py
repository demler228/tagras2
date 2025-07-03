from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_training_menu_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="Обучение", callback_data="education_button")
    builder.button(text="Викторина", callback_data="quiz_button")
    builder.button(
        text="🔙 Назад в меню",
        callback_data="back_to_main_menu"
    )

    builder.adjust(1)

    return builder.as_markup()