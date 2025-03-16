from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from application.tg_bot.faq.entities.faq import Faq

def get_faq_menu_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="Изменить вопрос", callback_data="faq_change_question_button")
    builder.button(text="Изменить ответ", callback_data="faq_change_answer_button")
    builder.button(text="Удалить вопрос-ответ", callback_data="faq_delete_button")
    builder.button(text="Назад", callback_data="faq_button_admin")

    builder.adjust(2,1)

    return builder.as_markup()