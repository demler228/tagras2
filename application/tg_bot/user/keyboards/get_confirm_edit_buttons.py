from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


class EmployeeCallback(CallbackData, prefix="employee"):
    action: str
    employee_id: int

def get_employee_list_keyboard(employees):
    builder = InlineKeyboardBuilder()

    for employee in employees:
        builder.button(
            text=f"{employee.username} ({employee.tg_username})",
            callback_data=EmployeeCallback(action="view", employee_id=employee.id)
        )
    builder.adjust(1)

    builder.row(InlineKeyboardButton(text="Назад", callback_data="get_admin_main_menu"))

    return builder.as_markup()


def get_confirm_edit_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Сохранить", callback_data="employee_save"),
            InlineKeyboardButton(text="✏️ Редактировать", callback_data="employee_edit"),
        ]
    ])

def get_edit_options_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📝 Имя", callback_data="edit_employee_name")],
        [InlineKeyboardButton(text="📞 Телефон", callback_data="edit_employee_phone")],
        [InlineKeyboardButton(text="📱 Username", callback_data="edit_employee_username")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="confirm_data_employee_back")],
    ])

def get_back_employee_button():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🔙 Назад", callback_data="employee_back_button"),
        ]
    ])


def get_employee_action_keyboard(employee_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text="✏️ Редактировать",
        callback_data=EmployeeCallback(action="edit", employee_id=employee_id)
    )

    builder.button(
        text="❌ Удалить",
        callback_data=EmployeeCallback(action="delete", employee_id=employee_id)
    )

    builder.row(InlineKeyboardButton(text="Назад", callback_data="get_employees_list_button"))

    return builder.as_markup()

