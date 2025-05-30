from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_employee_menu_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="Список сотрудников", callback_data="get_employees_list_button")
    builder.button(text="Назад", callback_data="get_admin_main_menu")

    builder.adjust(1)

    return builder.as_markup()

