from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from application.tg_bot.faq.entities.faq import Faq

class FaqCallback(CallbackData, prefix="faq"):
    faq_id: int

class FaqListCallback(CallbackData, prefix="faq_list"):
    page: int

def get_faq_list_keyboard(faq_list: list[Faq], page: int, questions_per_page: int = 5) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    start_index = (page - 1) * questions_per_page
    end_index = min(start_index + questions_per_page, len(faq_list))

    for faq in faq_list[start_index:end_index]:
        builder.button(text=faq.question, callback_data=FaqCallback(faq_id=faq.id))
    if page > 1:
        builder.button(text="⬅️ Назад", callback_data=FaqListCallback(page=page - 1))
    if (page * questions_per_page) < len(faq_list):
       builder.button(text="Вперед ➡️", callback_data=FaqListCallback(page=page + 1))
    builder.button(text="Добавить вопрос-ответ", callback_data="faq_create_button")
    builder.button(text="🔙 В меню", callback_data="back_to_admin_main_menu")
    builder.button(text=f"Страница {page}", callback_data="ignore")

    builder.adjust(1)
    if page > 1 and (page * questions_per_page) < len(faq_list):
        builder.adjust( *[1 for i in range(5)],2,1,1,1)

    return builder.as_markup()