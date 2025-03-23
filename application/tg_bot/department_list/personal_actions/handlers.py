from aiogram import Router, F
from aiogram.types import CallbackQuery

from .keyboards.callback_factories import DepartmentCallback, DepartmentEmployeeCallback
from .keyboards.department_keyboard import (
    get_department_list_keyboard,
    get_department_employee_list_keyboard,
    get_department_employee_detail_keyboard,
)

router = Router()


# Обработчик для списка отделов
@router.callback_query(F.data == "department_list_button")
async def handle_department_list_button(callback_query: CallbackQuery):
    await callback_query.message.edit_text(
        text="Список отделов:",
        reply_markup=get_department_list_keyboard()
    )

# Обработчик для просмотра сотрудников в отделе
@router.callback_query(DepartmentCallback.filter(F.action == "view"))
async def handle_view_department(callback: CallbackQuery, callback_data: DepartmentCallback):
    department_id = callback_data.department_id
    await callback.message.edit_text(
        text=f"Сотрудники отдела:",
        reply_markup=get_department_employee_list_keyboard(department_id)
    )

# Обработчик для просмотра деталей сотрудника
@router.callback_query(DepartmentEmployeeCallback.filter(F.action == "view"))
async def handle_view_employee(callback: CallbackQuery, callback_data: DepartmentEmployeeCallback):
    employee_id = callback_data.employee_id

    # Заглушка данных
    employee_details = {
        1: {"name": "Иван Иванов", "contact": "@ivanov", "department": "Отдел разработки", "department_id": 1},
        2: {"name": "Петр Петров", "contact": "@petrov", "department": "Отдел разработки", "department_id": 1},
        3: {"name": "Анна Сидорова", "contact": "@sidorova", "department": "Отдел маркетинга", "department_id": 2},
        4: {"name": "Мария Кузнецова", "contact": "@kuznetsova", "department": "Отдел маркетинга", "department_id": 2},
        5: {"name": "Сергей Сергеев", "contact": "@sergeev", "department": "Отдел продаж", "department_id": 3},
        6: {"name": "Ольга Ольгова", "contact": "@olgova", "department": "Отдел продаж", "department_id": 3},
    }

    employee = employee_details.get(employee_id)
    if employee:
        text = (
            f"👤 {employee['name']}\n\n"
            f"📞 Контакт: {employee['contact']}\n\n"
            f"🏢 Отдел: {employee['department']}"
        )
        await callback.message.edit_text(
            text=text,
            reply_markup=get_department_employee_detail_keyboard(employee_id, employee["department_id"])
        )
    else:
        await callback.message.edit_text("Сотрудник не найден.")