from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from application.tg_bot.faq.entities.faq import Faq

class FaqMenuCallback(CallbackData, prefix="faq_menu"):
    faq_id: int
    faq_list: list[Faq]

def get_theme_menu_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="Изменить название", callback_data="faq_change_question_button")
    builder.button(text="Изменить ответ", callback_data="faq_change_answer_button")
    builder.button(text="Удалить тему", callback_data="faq_delete_button")
    builder.button(text="Изменить материал", callback_data="faq_change_materials_button")
    builder.button(text="Назад", callback_data="training_button_admin")

    builder.adjust(1)

    return builder.as_markup()