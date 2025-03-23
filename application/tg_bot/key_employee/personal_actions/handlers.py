from aiogram import Router, F
from aiogram.types import CallbackQuery

from domain.key_employee.db_bl import KeyEmployeeDbBl
from utils.data_state import DataSuccess

from .keyboards.callback_factories import UserEmployeeCallback, UserPaginationCallback
from .keyboards.key_employee_keyboard import get_user_employee_list_keyboard, get_employee_detail_keyboard

router = Router()

@router.callback_query(F.data == "key_users_button")
async def handle_contacts_button(callback_query: CallbackQuery):
    data_state = KeyEmployeeDbBl.get_key_employee_list()
    if isinstance(data_state, DataSuccess):
        employees = data_state.data
        await callback_query.message.edit_text(
            text="Список полезных контактов:",
            reply_markup=get_user_employee_list_keyboard(employees, page=0)
        )
    else:
        await callback_query.message.answer("Ошибка при загрузке контактов.")

@router.callback_query(UserEmployeeCallback.filter(F.action == "view"))
async def handle_view_employee(callback: CallbackQuery, callback_data: UserEmployeeCallback):
    data_state = KeyEmployeeDbBl.get_key_employee_list()
    if isinstance(data_state, DataSuccess):
        employees = data_state.data
        employee = next((emp for emp in employees if emp.id == callback_data.employee_id), None)
        if employee:
            text = (
                f"👤 {employee.username}\n\n"
                f"📝 {employee.description}\n\n"
                f"💼 {employee.role}\n\n"
                f"📞 {employee.phone}"
            )
            if employee.telegram_username:
                text += f"\n\n🔗 {employee.telegram_username}"

            await callback.message.edit_text(
                text=text,
                reply_markup=get_employee_detail_keyboard(employee.id)
            )
        else:
            await callback.message.edit_text("Сотрудник не найден.")
    else:
        await callback.message.edit_text(f"Ошибка: {data_state.error_message}")

@router.callback_query(UserPaginationCallback.filter())
async def handle_pagination(callback: CallbackQuery, callback_data: UserPaginationCallback):
    data_state = KeyEmployeeDbBl.get_key_employee_list()
    if isinstance(data_state, DataSuccess):
        employees = data_state.data
        page = callback_data.page

        if callback_data.action == "next":
            page += 1
        elif callback_data.action == "prev":
            page -= 1

        await callback.message.edit_text(
            text="Список полезных контактов:",
            reply_markup=get_user_employee_list_keyboard(employees, page=page)
        )
    else:
        await callback.message.edit_text(f"Ошибка: {data_state.error_message}")