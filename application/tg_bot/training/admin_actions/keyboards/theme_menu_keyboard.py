from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from application.tg_bot.faq.entities.faq import Faq

def get_theme_menu_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="Создать материал", callback_data="theme_create_material_button")
    builder.button(text="Изменить название", callback_data="theme_change_name_button")
    builder.button(text="Изменить материалы", callback_data="theme_change_materials_button")
    builder.button(text="Удалить тему", callback_data="theme_delete_button")
    builder.button(text="Назад", callback_data="training_button_admin")

    builder.adjust(1,2,1)

    return builder.as_markup()

