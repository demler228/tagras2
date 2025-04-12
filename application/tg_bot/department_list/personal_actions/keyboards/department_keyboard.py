from aiogram.utils.keyboard import InlineKeyboardBuilder
from .callback_factories import (
    DepartmentCallback,
    DepartmentEmployeeCallback,
    DepartmentListCallback,
    DepartmentEmployeePageCallback)


def get_department_list_keyboard(departments: list, page: int = 1, per_page: int = 5):
    builder = InlineKeyboardBuilder()

    # Расчет диапазона отделов для текущей страницы
    start = (page - 1) * per_page
    end = start + per_page
    current_page_departments = departments[start:end]

    # Добавляем кнопки отделов
    for dept in current_page_departments:
        builder.button(
            text=dept.name,
            callback_data=DepartmentCallback(action="view", department_id=dept.id)
        )

    # Добавляем кнопки навигации
    if page > 1:
        builder.button(
            text="⬅️ Назад",
            callback_data=DepartmentListCallback(action="page", page=page - 1)
        )
    if end < len(departments):
        builder.button(
            text="Вперед ➡️",
            callback_data=DepartmentListCallback(action="page", page=page + 1)
        )

    # Возврат в главное меню
    builder.button(text="Назад в меню", callback_data="back_to_main_menu")

    builder.adjust(1)
    return builder.as_markup()


def get_department_employee_list_keyboard(employees: list, department_id: int, page: int = 1, per_page: int = 5):
    builder = InlineKeyboardBuilder()

    # Пагинация
    start = (page - 1) * per_page
    end = start + per_page
    current_page_employees = employees[start:end]

    for employee in current_page_employees:
        builder.button(
            text=employee.name,
            callback_data=DepartmentEmployeeCallback(
                action="view",
                employee_id=employee.id
            ),
        )

    # Навигация по страницам
    if page > 1:
        builder.button(
            text="⬅️ Назад",
            callback_data=DepartmentEmployeePageCallback(
                department_id=department_id,
                page=page - 1
            )
        )

    if end < len(employees):
        builder.button(
            text="Вперед ➡️",
            callback_data=DepartmentEmployeePageCallback(
                department_id=department_id,
                page=page + 1
            )
        )

    # Кнопки возврата
    builder.button(text="Назад к отделам", callback_data="department_list_button")
    builder.button(text="Назад в меню", callback_data="back_to_main_menu")

    builder.adjust(1)
    return builder.as_markup()


def get_department_employee_detail_keyboard(employee_id: int, department_id: int):
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Назад к сотрудникам",
        callback_data=DepartmentCallback(
            action="view",
            department_id=department_id
        ),
    )
    builder.button(text="Назад в меню", callback_data="back_to_main_menu")
    builder.adjust(1)
    return builder.as_markup()