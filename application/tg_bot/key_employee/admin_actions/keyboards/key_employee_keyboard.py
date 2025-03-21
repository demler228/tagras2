# application/tg_bot/key_employee/admin_actions/keyboards/keyboards.py
from aiogram.utils.keyboard import InlineKeyboardBuilder
from .callback_factories import EmployeeCallback, PaginationCallback, AdminActionCallback


def get_admin_main_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="Просмотреть сотрудников", callback_data=AdminActionCallback(action="view"))
    builder.button(text="Добавить сотрудника", callback_data=AdminActionCallback(action="add"))
    builder.button(text="Изменить сотрудника", callback_data=AdminActionCallback(action="edit"))
    builder.button(text="В главное меню", callback_data="back_to_admin_main_menu")
    builder.adjust(1)
    return builder.as_markup()


def get_employee_list_keyboard(employees: list, page: int, page_size: int = 3):
    builder = InlineKeyboardBuilder()

    # Кнопки сотрудников (одна строка на каждого сотрудника)
    for employee in employees[page * page_size:(page + 1) * page_size]:
        builder.button(
            text=employee.username,
            callback_data=EmployeeCallback(action="view", employee_id=employee.id)
        )

    # Кнопки пагинации (одна строка)
    pagination_buttons = []
    if page > 0:
        pagination_buttons.append(("⬅️ Назад", PaginationCallback(action="prev", page=page)))
    if (page + 1) * page_size < len(employees):
        pagination_buttons.append(("Вперёд ➡️", PaginationCallback(action="next", page=page)))

    for text, callback_data in pagination_buttons:
        builder.button(text=text, callback_data=callback_data)

    # Кнопки "Назад к действиям" и "В главное меню" (одна строка)
    builder.button(text="Назад к действиям", callback_data=AdminActionCallback(action="menu"))
    builder.button(text="В главное меню", callback_data="back_to_admin_main_menu")

    builder.adjust(1)

    return builder.as_markup()


def get_employee_detail_keyboard(employee_id: int):
    builder = InlineKeyboardBuilder()
    builder.button(text="Изменить", callback_data=EmployeeCallback(action="edit", employee_id=employee_id))
    builder.button(text="Удалить", callback_data=EmployeeCallback(action="delete", employee_id=employee_id))
    builder.button(text="Назад", callback_data=AdminActionCallback(action="view"))
    builder.adjust(1, 2)
    return builder.as_markup()

def get_employee_edit_keyboard(employee_id:int):
    builder = InlineKeyboardBuilder()
    builder.button(text="Изменить имя", callback_data=EmployeeCallback(action="edit_name", employee_id=employee_id))
    builder.button(text="Изменить описание",
                   callback_data=EmployeeCallback(action="edit_description", employee_id=employee_id))
    builder.button(text="Изменить должность",
                   callback_data=EmployeeCallback(action="edit_role", employee_id=employee_id))
    builder.button(text="Изменить телефон",
                   callback_data=EmployeeCallback(action="edit_phone", employee_id=employee_id))
    builder.button(text="Изменить Telegram",
                   callback_data=EmployeeCallback(action="edit_telegram", employee_id=employee_id))

    # Кнопки "Назад к действиям" и "В главное меню"
    builder.button(text="Назад к действиям", callback_data=AdminActionCallback(action="menu"))
    builder.button(text="В главное меню", callback_data="back_to_admin_main_menu")

    # Настройка расположения кнопок
    builder.adjust(1)
    return builder.as_markup()

def get_employee_delete_keyboard(employee_id:int):
    builder = InlineKeyboardBuilder()
    builder.button(text="Да, удалить",
                   callback_data=EmployeeCallback(action="confirm_delete", employee_id=employee_id))
    builder.button(text="Нет, отменить",
                   callback_data=EmployeeCallback(action="view", employee_id=employee_id))

    builder.button(text="Назад к действиям", callback_data=AdminActionCallback(action="menu"))
    builder.button(text="В главное меню", callback_data="back_to_admin_main_menu")

    builder.adjust(1)
    return builder.as_markup()