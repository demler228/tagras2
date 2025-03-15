from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from application.tg_bot.training.entities.materials import Material

class ThemeChooseMaterialsCallback(CallbackData, prefix="theme_menu"):
    material_id: int

def get_theme_choose_materials_keyboard(materials: list[Material]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for i, material in enumerate(materials):
        builder.button(text=str(i), callback_data=ThemeChooseMaterialsCallback(material_id=material.id))
    builder.button(text="Назад", callback_data='back_theme_button')

    builder.adjust(*[4 for i in range(len(materials)//4)],len(materials)%4 if len(materials)%4 != 0 else 1 ,1)

    return builder.as_markup()