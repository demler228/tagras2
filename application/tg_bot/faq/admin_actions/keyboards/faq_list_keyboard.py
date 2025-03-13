from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from application.tg_bot.faq.entities.faq import Faq

class FaqCallback(CallbackData, prefix="faq"):
    faq_id: int

def get_faq_list_keyboard(faq_list: list[Faq]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="Добавить вопрос-ответ", callback_data="faq_create_button")

    for faq in faq_list:
        builder.button(text=faq.question, callback_data=FaqCallback(faq_id=faq.id))
    builder.button(text="Назад", callback_data="back_to_admin_main_menu")

    builder.adjust(1)

    return builder.as_markup()