from aiogram.utils.keyboard import InlineKeyboardBuilder
from .callback_factories import DepartmentCallback, DepartmentEmployeeCallback

# Заглушка данных
departments = [
    {"id": 1, "name": "Отдел разработки"},
    {"id": 2, "name": "Отдел маркетинга"},
    {"id": 3, "name": "Отдел продаж"},
]

employees = {
    1: [
        {"id": 1, "name": "Иван Иванов", "contact": "@ivanov"},
        {"id": 2, "name": "Петр Петров", "contact": "@petrov"},
    ],
    2: [
        {"id": 3, "name": "Анна Сидорова", "contact": "@sidorova"},
        {"id": 4, "name": "Мария Кузнецова", "contact": "@kuznetsova"},
    ],
    3: [
        {"id": 5, "name": "Сергей Сергеев", "contact": "@sergeev"},
        {"id": 6, "name": "Ольга Ольгова", "contact": "@olgova"},
    ],
}

# Клавиатура для списка отделов
def get_department_list_keyboard():
    builder = InlineKeyboardBuilder()

    for department in departments:
        builder.button(
            text=department["name"],
            callback_data=DepartmentCallback(action="view", department_id=department["id"])
        )

    # Кнопка "Назад в меню"
    builder.button(text="Назад в меню", callback_data="back_to_main_menu")
    builder.adjust(1)
    return builder.as_markup()

# Клавиатура для списка сотрудников в отделе
def get_department_employee_list_keyboard(department_id: int):
    builder = InlineKeyboardBuilder()

    for employee in employees.get(department_id, []):
        builder.button(
            text=employee["name"],
            callback_data=DepartmentEmployeeCallback(action="view", employee_id=employee["id"])
        )

    # Кнопка "Назад к отделам"
    builder.button(text="Назад к отделам", callback_data="department_list_button")

    # Кнопка "Назад в меню"
    builder.button(text="Назад в меню", callback_data="back_to_main_menu")
    builder.adjust(1)
    return builder.as_markup()

# Клавиатура для деталей сотрудника
def get_department_employee_detail_keyboard(employee_id: int, department_id: int):
    builder = InlineKeyboardBuilder()

    # Кнопка "Назад к сотрудникам"
    builder.button(
        text="Назад к сотрудникам",
        callback_data=DepartmentCallback(action="view", department_id=department_id)
    )

    # Кнопка "Назад в меню"
    builder.button(text="Назад в меню", callback_data="back_to_main_menu")
    builder.adjust(1)
    return builder.as_markup()