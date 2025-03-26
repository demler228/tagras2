from aiogram.utils.keyboard import InlineKeyboardBuilder
from .callback_factories import UserEmployeeCallback, UserPaginationCallback

def get_user_employee_list_keyboard(employees: list, page: int, page_size: int = 3):
    builder = InlineKeyboardBuilder()

    # Кнопки сотрудников
    for employee in employees[page * page_size:(page + 1) * page_size]:
        builder.button(
            text=employee.username,
            callback_data=UserEmployeeCallback(action="view", employee_id=employee.id)
        )

    # Кнопки пагинации
    pagination_buttons = []
    if page > 0:
        pagination_buttons.append(("⬅️ Назад", UserPaginationCallback(action="prev", page=page)))
    if (page + 1) * page_size < len(employees):
        pagination_buttons.append(("Вперёд ➡️", UserPaginationCallback(action="next", page=page)))

    for text, callback_data in pagination_buttons:
        builder.button(text=text, callback_data=callback_data)

    # Кнопка "Назад в меню"
    builder.button(text="Назад в меню", callback_data="back_to_main_menu")

    builder.adjust(1)
    return builder.as_markup()

def get_employee_detail_keyboard(employee_id: int):
    builder = InlineKeyboardBuilder()
    builder.button(text="◀️ Назад к списку", callback_data="key_users_button")
    builder.button(text="Назад в меню", callback_data="back_to_main_menu")
    builder.adjust(1)
    return builder.as_markup()