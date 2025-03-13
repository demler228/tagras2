from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from application.tg_bot.faq.entities.faq import Faq


def get_faq_keyboard(faq_list: list[Faq]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="Добавить вопрос-ответ", callback_data="faq_create_button")

    for faq in faq_list:
        builder.button(text=faq.question, callback_data=f"faq_question_button-{faq.id}")
    builder.button(text="Назад", callback_data="back_to_admin_main_menu")

    builder.adjust(1)

    return builder.as_markup()