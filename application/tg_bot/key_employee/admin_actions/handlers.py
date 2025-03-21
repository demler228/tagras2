from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from utils.data_state import DataSuccess, DataFailedMessage

from domain.key_employee.db_bl import KeyEmployeeDbBl
from .keyboards import (
    EmployeeCallback,
    PaginationCallback,
    AdminActionCallback,
    get_admin_main_keyboard,
    get_employee_list_keyboard,
    get_employee_detail_keyboard
)
from ..entities import KeyEmployee

router = Router()


class AddEmployeeStates(StatesGroup):
    username = State()
    description = State()
    phone = State()
    role = State()


@router.callback_query(F.data == "contacts_button_admin")
async def handle_admin_menu(callback: CallbackQuery):
    await callback.message.answer(
        "Выберите действие:",
        reply_markup=get_admin_main_keyboard()
    )

@router.callback_query(AdminActionCallback.filter(F.action == "menu"))
async def handle_admin_menu(callback: CallbackQuery):
    await callback.message.edit_text(
        "Выберите действие:",
        reply_markup=get_admin_main_keyboard()
    )


@router.callback_query(AdminActionCallback.filter(F.action == "view"))
async def handle_view_employees(callback: CallbackQuery, state: FSMContext):
    data_state = KeyEmployeeDbBl.get_key_employee_list()
    if isinstance(data_state, DataSuccess):
        employees = data_state.data
        await callback.message.edit_text(
            "Список сотрудников:",
            reply_markup=get_employee_list_keyboard(employees, page=0)
        )
    else:
        await callback.message.edit_text(f"Ошибка: {data_state.error_message}")


@router.callback_query(PaginationCallback.filter())
async def handle_pagination(callback: CallbackQuery, callback_data: PaginationCallback, state: FSMContext):
    data_state = KeyEmployeeDbBl.get_key_employee_list()
    if isinstance(data_state, DataSuccess):
        employees = data_state.data
        page = callback_data.page
        if callback_data.action == "next":
            page += 1
        elif callback_data.action == "prev":
            page -= 1

        await callback.message.edit_text(
            "Список сотрудников:",
            reply_markup=get_employee_list_keyboard(employees, page=page)
        )


@router.callback_query(EmployeeCallback.filter(F.action == "view"))
async def handle_view_employee(callback: CallbackQuery, callback_data: EmployeeCallback):
    data_state = KeyEmployeeDbBl.get_key_employee_list()
    if isinstance(data_state, DataSuccess):
        employees = data_state.data
        employee = next((emp for emp in employees if emp.id == callback_data.employee_id), None)
        if employee:
            await callback.message.edit_text(
                f"👤 {employee.username}\n\n"
                f"📝 {employee.description}\n\n"
                f"📞 {employee.phone}\n\n"
                f"💼 {employee.role}",
                reply_markup=get_employee_detail_keyboard(employee.id)
            )
        else:
            await callback.message.edit_text("Сотрудник не найден.")
    else:
        await callback.message.edit_text(f"Ошибка: {data_state.error_message}")


@router.callback_query(AdminActionCallback.filter(F.action == "add"))
async def handle_add_employee(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Введите username сотрудника:")
    await state.set_state(AddEmployeeStates.username)


@router.message(AddEmployeeStates.username)
async def process_username(message: Message, state: FSMContext):
    await state.update_data(username=message.text)
    await message.answer("Введите описание сотрудника:")
    await state.set_state(AddEmployeeStates.description)


@router.message(AddEmployeeStates.description)
async def process_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer("Введите телефон сотрудника:")
    await state.set_state(AddEmployeeStates.phone)


@router.message(AddEmployeeStates.phone)
async def process_phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await message.answer("Введите роль сотрудника:")
    await state.set_state(AddEmployeeStates.role)


# async def get_telegram_id_by_username(bot: Bot, username: str) -> int | None:
#     try:
#         user = await bot.get_chat(f"@{username.lstrip('@')}")
#         return user.id
#     except Exception as e:
#         print(f"Ошибка при получении telegram_id: {e}")
#         return None

@router.message(AddEmployeeStates.role)
async def process_role(message: Message, state: FSMContext):
    user_data = await state.get_data()
    key_employee = KeyEmployee(
        telegram_id=0,  # Здесь можно добавить логику для получения telegram_id
        username=user_data['username'],
        description=user_data['description'],
        phone=user_data['phone'],
        role=message.text
    )
    data_state = KeyEmployeeDbBl.key_employee_create(key_employee)
    if isinstance(data_state, DataSuccess):
        await message.answer(f"Сотрудник {user_data['username']} успешно добавлен!")
    else:
        await message.answer(f"Ошибка: {data_state.error_message}")
    await state.clear()

@router.callback_query(AdminActionCallback.filter(F.action == "go_to_main_menu"))
async def handle_go_to_main_menu(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()