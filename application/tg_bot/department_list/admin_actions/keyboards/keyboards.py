from aiogram.utils.keyboard import InlineKeyboardBuilder
from .callback_factories import AdminActionCallback

def get_admin_menu_keyboard():
    builder = InlineKeyboardBuilder()

    # Кнопки для действий с отделами
    builder.button(
        text="Просмотр отделов",
        callback_data=AdminActionCallback(action="view_departments")
    )
    builder.button(
        text="Добавить отдел",
        callback_data=AdminActionCallback(action="add_department")
    )
    builder.button(
        text="Изменить отдел",
        callback_data=AdminActionCallback(action="edit_department")
    )
    builder.button(
        text="Удалить отдел",
        callback_data=AdminActionCallback(action="delete_department")
    )

    # Кнопки для действий с сотрудниками
    builder.button(
        text="Просмотр сотрудников",
        callback_data=AdminActionCallback(action="view_employees")
    )
    builder.button(
        text="Добавить сотрудника",
        callback_data=AdminActionCallback(action="add_employee")
    )
    builder.button(
        text="Изменить сотрудника",
        callback_data=AdminActionCallback(action="edit_employee")
    )
    builder.button(
        text="Удалить сотрудника",
        callback_data=AdminActionCallback(action="delete_employee")
    )

    builder.adjust(1)
    return builder.as_markup()
