from aiogram.utils.keyboard import InlineKeyboardBuilder
from .callback_factories import (
    AdminDepartmentListCallback,
    AdminDepartmentCallback,
    AdminDepartmentEmployeeCallback,
    AdminDepartmentEmployeePageCallback,
    AdminConfirmCallback,
    AdminEmployeeEditFieldCallback,
)


def get_department_list_keyboard(departments, page, admin=False, per_page=5):
    builder = InlineKeyboardBuilder()
    start = (page - 1) * per_page
    end = start + per_page
    current = departments[start:end]

    for dept in current:
        builder.button(
            text=dept.name,
            callback_data=AdminDepartmentCallback(action="view", department_id=dept.id),
        )

    if page > 1:
        builder.button(
            text="⬅️ Назад",
            callback_data=AdminDepartmentListCallback(action="page", page=page - 1),
        )

    if end < len(departments):
        builder.button(
            text="Вперед ➡️",
            callback_data=AdminDepartmentListCallback(action="page", page=page + 1)
        )

    if admin:
        builder.button(
            text="➕ Добавить отдел",
            callback_data="add_department_button"
        )

    builder.button(
        text="🔙 Назад в меню",
        callback_data="back_to_admin_main_menu"
    )

    builder.adjust(1)
    return builder.as_markup()


def get_department_employee_list_keyboard(
    employees, department_id, page, admin=False, per_page=5
):
    builder = InlineKeyboardBuilder()
    start = (page - 1) * per_page
    end = start + per_page

    for emp in employees[start:end]:
        builder.button(
            text=emp.name,
            callback_data=AdminDepartmentEmployeeCallback(
                action="view", employee_id=emp.id
            ),
        )
    if page > 1:
        builder.button(
            text="⬅️ Назад",
            callback_data=AdminDepartmentEmployeePageCallback(
                department_id=department_id, page=page - 1
            ),
        )
    if end < len(employees):
        builder.button(
            text="➡️ Вперед",
            callback_data=AdminDepartmentEmployeePageCallback(
                department_id=department_id, page=page + 1
            ),
        )
    if admin:
        builder.button(
            text="➕ Добавить сотрудника",
            callback_data=AdminDepartmentCallback(
                action="add_employee", department_id=department_id
            ),
        )
        builder.button(
            text="➕ Удалить отдел",
            callback_data=AdminDepartmentCallback(
                action="delete", department_id=department_id
            ),
        )
    builder.button(
        text="🔙 Назад к отделам",
        callback_data="department_list_button_admin"
    )
    builder.adjust(1)
    return builder.as_markup()


def get_department_employee_detail_keyboard(employee_id: int, department_id: int, admin=False):
    builder = InlineKeyboardBuilder()

    if admin:
        builder.button(
            text="✏️ Изменить",
            callback_data=AdminDepartmentEmployeeCallback(
                action="edit",
                employee_id=employee_id
            )
        )
        builder.button(
            text="🗑 Удалить",
            callback_data=AdminDepartmentEmployeeCallback(
                action="delete",
                employee_id=employee_id
            )
        )

    builder.button(
        text="🔙 Назад",
        callback_data=AdminDepartmentCallback(
            action="view",
            department_id=department_id
        )
    )
    builder.adjust(1)
    return builder.as_markup()


def get_confirm_delete_keyboard(entity_id, target):
    builder = InlineKeyboardBuilder()
    builder.button(
        text="✅ Подтвердить",
        callback_data=AdminConfirmCallback(target=target, entity_id=entity_id),
    )
    builder.button(
        text="❌ Отмена",
        callback_data="department_list_button_admin"
    )
    builder.adjust(1)
    return builder.as_markup()


def get_employee_edit_fields_keyboard(employee_id: int):
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Изменить имя",
        callback_data=AdminEmployeeEditFieldCallback(
            field="name",
            employee_id=employee_id
        )
    )
    builder.button(
        text="Изменить телефон",
        callback_data=AdminEmployeeEditFieldCallback(
            field="phone",
            employee_id=employee_id
        )
    )
    builder.button(
        text="Изменить описание",
        callback_data=AdminEmployeeEditFieldCallback(
            field="description",
            employee_id=employee_id
        )
    )
    builder.button(
        text="🔙 Назад",
        callback_data=AdminDepartmentEmployeeCallback(
            action="view",
            employee_id=employee_id
        )
    )
    builder.adjust(1)
    return builder.as_markup()

def get_cancel_keyboard(callback_data: str = "department_list_button_admin"):
    builder = InlineKeyboardBuilder()
    builder.button(
        text="🔙 Отмена",
        callback_data=callback_data
    )
    return builder.as_markup()

def back_to_dept():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="🔙 Назад к отделам",
        callback_data="department_list_button_admin"
    )
    return builder.as_markup()

def back_to_employees(department_id):
    # Создаем клавиатуру для ответа
    builder = InlineKeyboardBuilder()
    builder.button(
        text="🔙 К списку сотрудников",
        callback_data=AdminDepartmentCallback(
            action="view",
            department_id=department_id
        )
    )
    return builder.as_markup()

def get_confirm_delete_keyboard(entity_id: int, target: str):
    builder = InlineKeyboardBuilder()
    builder.button(
        text="✅ Да, удалить",
        callback_data=AdminConfirmCallback(
            target=target,
            entity_id=entity_id
        )
    )
    builder.button(
        text="❌ Нет, отмена",
        callback_data=AdminDepartmentEmployeeCallback(
            action="view",
            employee_id=entity_id
        )
    )
    return builder.as_markup()

def back_to_employee_view(employee_id: int, department_id: int):
    builder = InlineKeyboardBuilder()
    builder.button(
        text="🔙 К карточке сотрудника",
        callback_data=AdminDepartmentEmployeeCallback(
            action="view",
            employee_id=employee_id
        )
    )
    builder.button(
        text="📋 К списку сотрудников",
        callback_data=AdminDepartmentCallback(
            action="view",
            department_id=department_id
        )
    )
    return builder.as_markup()