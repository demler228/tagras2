from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.exceptions import TelegramBadRequest
from utils.data_state import DataSuccess, DataState

from domain.department_list.db_bl import DepartmentDbBl, EmployeeDbBl
from .keyboards.callback_factories import (
    DepartmentCallback,
    DepartmentEmployeeCallback,
    DepartmentListCallback,
    DepartmentEmployeePageCallback)

from .keyboards.department_keyboard import (
    get_department_list_keyboard,
    get_department_employee_list_keyboard,
    get_department_employee_detail_keyboard,
)

router = Router()

@router.callback_query(F.data.startswith("departments_page:"))
@router.callback_query(F.data == "department_list_button")
async def handle_department_list(callback_query: CallbackQuery):
    # Определяем страницу
    if callback_query.data == "department_list_button":
        page = 1
    else:
        # Парсим callback_data через фабрику
        callback_data = DepartmentListCallback.unpack(callback_query.data)
        page = callback_data.page

    # Получаем отделы
    departments_state = DepartmentDbBl.get_department_list()
    if not isinstance(departments_state, DataSuccess):
        await callback_query.answer("Ошибка загрузки отделов")
        return

    departments = departments_state.data

    try:
        await callback_query.message.edit_text(
            text="Список отделов:",
            reply_markup=get_department_list_keyboard(departments, page=page)
        )
    except TelegramBadRequest as e:
        await callback_query.answer("Невозможно обновить сообщение")

@router.callback_query(DepartmentEmployeePageCallback.filter())
@router.callback_query(DepartmentCallback.filter(F.action == "view"))
async def handle_department_employees(
    callback: CallbackQuery,
    callback_data: DepartmentCallback | DepartmentEmployeePageCallback,
):
    # Определим department_id и нужную страницу
    department_id = callback_data.department_id
    page = getattr(callback_data, "page", 1)  # по умолчанию первая страница

    employees_state = EmployeeDbBl.get_employee_list(department_id)
    if not isinstance(employees_state, DataSuccess):
        await callback.answer("Ошибка загрузки сотрудников")
        return

    employees = employees_state.data
    if not employees:
        await callback.answer("В этом отделе пока нет сотрудников")
        return

    try:
        await callback.message.edit_text(
            text="Сотрудники отдела:",
            reply_markup=get_department_employee_list_keyboard(
                employees=employees,
                department_id=department_id,
                page=page
            )
        )
    except Exception as e:
        await callback.answer(f"Ошибка: {str(e)}")


@router.callback_query(DepartmentEmployeeCallback.filter(F.action == "view"))
async def handle_view_employee(
        callback: CallbackQuery,
        callback_data: DepartmentEmployeeCallback
):
    employee_state = EmployeeDbBl.get_employee_details(callback_data.employee_id)

    if not isinstance(employee_state, DataSuccess):
        await callback.message.edit_text("Ошибка при получении данных сотрудника")
        return

    employee = employee_state.data
    await callback.message.edit_text(
        text=(
            f"👤 {employee.name}\n\n"
            f"📞 Телефон: {employee.phone or 'не указан'}\n\n"
            f"📝 Описание: {employee.description or 'нет описания'}\n\n"
        ),
        reply_markup=get_department_employee_detail_keyboard(
            employee_id=employee.id,
            department_id=employee.department_id
        )
    )
