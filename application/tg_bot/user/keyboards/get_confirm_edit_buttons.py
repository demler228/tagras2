from typing import List

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from application.tg_bot.user.entities.user import User



class EmployeeCallback(CallbackData, prefix="employee"):
    action: str
    employee_id: int


class EmployeesCallbackFactory(CallbackData, prefix="employees"):
    offset: int


def get_employees_list_keyboard(employees: List[User], offset: int = 0, page_size: int = 10) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    # Вычисляем начало и конец текущей страницы
    start_idx = offset * page_size
    end_idx = start_idx + page_size
    total_employees = len(employees)

    # Показываем сотрудников для текущей страницы
    for employee in employees[start_idx:end_idx]:
        builder.button(
            text=f"{employee.username}",
            callback_data=EmployeeCallback(action="view", employee_id=employee.id).pack()
        )

    # Добавляем кнопки навигации
    if offset > 0:
        builder.button(
            text="<--- ",
            callback_data=EmployeesCallbackFactory(offset=offset - 1)
        )

    if end_idx < total_employees:
        builder.button(
            text=" --->",
            callback_data=EmployeesCallbackFactory(offset=offset + 1)
        )

    builder.button(
        text="🔙 В меню",
        callback_data="employee_back_button"
    )

    # Организуем кнопки: сотрудники по одному в строке, навигация в одной строке, кнопка меню отдельно
    builder.adjust(1, 2 if offset > 0 and end_idx < total_employees else 1, 1)

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
        [InlineKeyboardButton(text="🔢 Telegram id", callback_data="edit_employee_telegram_id")],
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


