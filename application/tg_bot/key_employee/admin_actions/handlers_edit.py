# application/tg_bot/key_employee/admin_actions/handlers_edit.py
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State

from domain.key_employee.db_bl import KeyEmployeeDbBl
from ..entities import KeyEmployee
from utils.data_state import DataSuccess

from .keyboards import (
    EmployeeCallback,
    get_employee_edit_keyboard,
    get_admin_main_keyboard
)

# Создаем роутер для редактирования
router = Router()

# Состояния для редактирования
class EditEmployeeStates(StatesGroup):
    username = State()
    description = State()
    phone = State()
    role = State()
    telegram_username = State()

# Обработчик для выбора поля для редактирования
@router.callback_query(EmployeeCallback.filter(F.action == "edit_field"))
async def handle_edit_field(callback: CallbackQuery, callback_data: EmployeeCallback, state: FSMContext):
    await state.update_data(employee_id=callback_data.employee_id)
    await callback.message.edit_text(
        text="Выберите поле для редактирования:",
        reply_markup=get_employee_edit_keyboard(callback_data.employee_id)
    )

# Обработчики для выбора конкретного поля
@router.callback_query(EmployeeCallback.filter(F.action == "edit_name"))
async def handle_edit_name(callback: CallbackQuery, callback_data: EmployeeCallback, state: FSMContext):
    await state.update_data(employee_id=callback_data.employee_id)
    await callback.message.edit_text("Введите новое имя сотрудника:")
    await state.set_state(EditEmployeeStates.username)

@router.callback_query(EmployeeCallback.filter(F.action == "edit_description"))
async def handle_edit_description(callback: CallbackQuery, callback_data: EmployeeCallback, state: FSMContext):
    await state.update_data(employee_id=callback_data.employee_id)
    await callback.message.edit_text("Введите новое описание сотрудника:")
    await state.set_state(EditEmployeeStates.description)

@router.callback_query(EmployeeCallback.filter(F.action == "edit_phone"))
async def handle_edit_phone(callback: CallbackQuery, callback_data: EmployeeCallback, state: FSMContext):
    await state.update_data(employee_id=callback_data.employee_id)
    await callback.message.edit_text("Введите новый телефон сотрудника:")
    await state.set_state(EditEmployeeStates.phone)

@router.callback_query(EmployeeCallback.filter(F.action == "edit_role"))
async def handle_edit_role(callback: CallbackQuery, callback_data: EmployeeCallback, state: FSMContext):
    await state.update_data(employee_id=callback_data.employee_id)
    await callback.message.edit_text("Введите новую роль сотрудника:")
    await state.set_state(EditEmployeeStates.role)

@router.callback_query(EmployeeCallback.filter(F.action == "edit_telegram"))
async def handle_edit_telegram(callback: CallbackQuery, callback_data: EmployeeCallback, state: FSMContext):
    await state.update_data(employee_id=callback_data.employee_id)
    await callback.message.edit_text(
        "Введите новый Telegram username сотрудника (например, @username) или введите \"-\" для пропуска этого поля:"
    )
    await state.set_state(EditEmployeeStates.telegram_username)

# Универсальный обработчик для сохранения изменений
async def process_edit_field(message: Message, state: FSMContext, field_name: str):
    # Получаем данные из состояния
    user_data = await state.get_data()
    employee_id = user_data.get('employee_id')
    new_value = message.text.strip()

    # Если поле telegram_username и введен "-", сохраняем None
    if field_name == 'telegram_username' and new_value in ("-", ""):
        new_value = None

    # Проверяем, что employee_id существует
    if not employee_id:
        await message.answer("Ошибка: не удалось определить сотрудника для редактирования.")
        await state.clear()
        return

    # Получаем текущие данные сотрудника
    data_state = KeyEmployeeDbBl.get_key_employee_list()
    if isinstance(data_state, DataSuccess):
        employees = data_state.data
        employee = next((emp for emp in employees if emp.id == employee_id), None)
        if employee:
            # Обновляем поле
            setattr(employee, field_name, new_value)
            # Сохраняем изменения
            data_state = KeyEmployeeDbBl.key_employee_update(employee)
            if isinstance(data_state, DataSuccess):
                await message.answer(
                    text=f"{field_name.capitalize()} сотрудника успешно обновлено!",
                    reply_markup=get_admin_main_keyboard()  # Показываем меню выбора действия
                )
            else:
                await message.answer(
                    text=f"Ошибка: {data_state.error_message}",
                    reply_markup=get_admin_main_keyboard()
                )
        else:
            await message.answer("Сотрудник не найден.")
    else:
        await message.answer(f"Ошибка: {data_state.error_message}")

    # Очищаем состояние после завершения
    await state.clear()

# Обработчики для каждого поля
@router.message(EditEmployeeStates.username)
async def process_edit_username(message: Message, state: FSMContext):
    await process_edit_field(message, state, 'username')

@router.message(EditEmployeeStates.description)
async def process_edit_description(message: Message, state: FSMContext):
    await process_edit_field(message, state, 'description')

@router.message(EditEmployeeStates.phone)
async def process_edit_phone(message: Message, state: FSMContext):
    await process_edit_field(message, state, 'phone')

@router.message(EditEmployeeStates.role)
async def process_edit_role(message: Message, state: FSMContext):
    await process_edit_field(message, state, 'role')

@router.message(EditEmployeeStates.telegram_username)
async def process_edit_telegram_username(message: Message, state: FSMContext):
    await process_edit_field(message, state, 'telegram_username')