# application/tg_bot/key_employee/admin_actions/keyboards/keyboards.py
from aiogram.utils.keyboard import InlineKeyboardBuilder
from .callback_factories import EmployeeCallback, PaginationCallback, AdminActionCallback


def get_admin_main_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="Просмотреть сотрудников", callback_data=AdminActionCallback(action="view"))
    builder.button(text="Добавить сотрудника", callback_data=AdminActionCallback(action="add"))
    builder.button(text="Изменить сотрудника", callback_data=AdminActionCallback(action="edit"))
    builder.button(text="В главное меню", callback_data=AdminActionCallback(action="go_to_main_menu"))
    builder.adjust(1)
    return builder.as_markup()


def get_employee_list_keyboard(employees: list, page: int, page_size: int = 3):
    builder = InlineKeyboardBuilder()

    # Кнопки сотрудников
    for employee in employees[page * page_size:(page + 1) * page_size]:
        builder.button(
            text=employee.username,
            callback_data=EmployeeCallback(action="view", employee_id=employee.id)
        )

    # Кнопки пагинации
    if page > 0:
        builder.button(text="⬅️ Назад", callback_data=PaginationCallback(action="prev", page=page))
    if (page + 1) * page_size < len(employees):
        builder.button(text="Вперёд ➡️", callback_data=PaginationCallback(action="next", page=page))

    # Кнопки меню
    builder.button(text="Назад к действиям", callback_data=AdminActionCallback(action="menu"))
    builder.adjust(1, 2, 1)
    return builder.as_markup()


def get_employee_detail_keyboard(employee_id: int):
    builder = InlineKeyboardBuilder()
    builder.button(text="Изменить", callback_data=EmployeeCallback(action="edit", employee_id=employee_id))
    builder.button(text="Удалить", callback_data=EmployeeCallback(action="delete", employee_id=employee_id))
    builder.button(text="Назад", callback_data=AdminActionCallback(action="view"))
    builder.adjust(1, 2)
    return builder.as_markup()