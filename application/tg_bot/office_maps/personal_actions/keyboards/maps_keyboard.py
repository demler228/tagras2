from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_office_maps_keyboard():
    """
    Создает клавиатуру для выбора этажа.
    """
    builder = InlineKeyboardBuilder()

    # Кнопки для выбора этажа
    builder.button(text="1 этаж", callback_data="office_map_1")
    builder.button(text="2 этаж", callback_data="office_map_2")
    builder.button(text="3 этаж", callback_data="office_map_3")

    # Кнопка "Назад в меню"
    builder.button(text="🔙 В меню", callback_data="back_to_menu")

    # Настройка расположения кнопок
    builder.adjust(1)
    return builder.as_markup()


def get_office_map_keyboard(floor: str):
    """
    Создает клавиатуру для возврата к выбору этажа.
    """
    builder = InlineKeyboardBuilder()
    builder.button(
        text="🔙 К выбору этажа",
        callback_data="back_to_floors"
    )
    builder.button(text="🔙 В меню", callback_data="back_to_menu")
    builder.adjust(1)
    return builder.as_markup()