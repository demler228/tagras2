from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from application.tg_bot.faq.entities.faq import Faq

def get_theme_material_menu_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="Изменить название", callback_data="change_material_name_button")
    builder.button(text="Изменить url", callback_data="change_material_url_button")
    builder.button(text="Удалить материал", callback_data="material_delete_button")
    builder.button(text="Назад", callback_data="back_theme_choose_materials")

    builder.adjust(2,1)

    return builder.as_markup()

