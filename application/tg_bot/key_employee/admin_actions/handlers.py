from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, contact
from aiogram.fsm.state import StatesGroup, State
from numpy.f2py.cfuncs import callbacks
from utils.data_state import DataSuccess, DataFailedMessage

from domain.key_employee.db_bl import KeyEmployeeDbBl
from utils.logs import admin_logger
from .keyboards import (
    EmployeeCallback,
    PaginationCallback,
    AdminActionCallback,
    get_admin_main_keyboard,
    get_employee_list_keyboard,
    get_employee_detail_keyboard,
    get_employee_delete_keyboard,
    get_employee_edit_keyboard
)
from ..entities import KeyEmployee

router = Router()


class AddEmployeeStates(StatesGroup):
    username = State()
    description = State()
    phone = State()
    role = State()
    telegram_username = State()


@router.callback_query(AdminActionCallback.filter(F.action == "menu"))
@router.callback_query(F.data == "contacts_button_admin")
async def handle_admin_menu(callback: CallbackQuery):
    await callback.message.edit_text(
        "Выберите действие:",
        reply_markup=get_admin_main_keyboard()
    )


# @router.callback_query(AdminActionCallback.filter(F.action == "menu"))
# async def handle_admin_menu(callback: CallbackQuery):
#     await callback.message.edit_text(
#         "Выберите действие:",
#         reply_markup=get_admin_main_keyboard()
#     )

@router.callback_query(AdminActionCallback.filter(F.action == "edit"))
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
            text = (f"👤 {employee.username}\n\n"
                    f"📝 {employee.description}\n\n"
                    f"💼 {employee.role}\n\n"
                    f"📞 {employee.phone}")
            if employee.telegram_username != None:
                text += f"\n\n🔗 {employee.telegram_username}"
            await callback.message.edit_text(
                text=text,
                reply_markup=get_employee_detail_keyboard(employee.id)
            )
        else:
            await callback.message.edit_text("Сотрудник не найден.")
    else:
        await callback.message.edit_text(f"Ошибка: {data_state.error_message}")


@router.callback_query(AdminActionCallback.filter(F.action == "add"))
async def handle_add_employee(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Введите ФИО сотрудника:")
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


@router.message(AddEmployeeStates.role)
async def process_role(message: Message, state: FSMContext):
    await state.update_data(role=message.text)
    await message.answer("Введите username Telegram сотрудника (например, @username) "
                         "или введите \"-\" для пропуска этого поля:")
    await state.set_state(AddEmployeeStates.telegram_username)


@router.message(AddEmployeeStates.telegram_username)
async def process_telegram_username(message: Message, state: FSMContext):
    user_data = await state.get_data()
    telegram_username = message.text.strip()

    if telegram_username in ("-", ""):
        telegram_username = None

    key_employee = KeyEmployee(
        telegram_username=telegram_username,
        username=user_data['username'],
        description=user_data['description'],
        phone=user_data['phone'],
        role=user_data['role']
    )

    data_state = KeyEmployeeDbBl.key_employee_create(key_employee)
    if isinstance(data_state, DataSuccess):
        admin_logger.info(
            f'Админ {message.chat.full_name} ({message.chat.id} добавил сотрудника {key_employee.username})')
        await message.answer(
            text=f"Сотрудник {user_data['username']} успешно добавлен!",
            reply_markup=get_admin_main_keyboard()
        )
    else:
        await message.answer(
            text=f"Ошибка: {data_state.error_message}",
            reply_markup=get_admin_main_keyboard()
        )
    await state.clear()


@router.callback_query(EmployeeCallback.filter(F.action == "edit"))
async def handle_edit_employee(callback: CallbackQuery, callback_data: EmployeeCallback):
    data_state = KeyEmployeeDbBl.get_key_employee_list()
    if isinstance(data_state, DataSuccess):
        employees = data_state.data
        employee = next((emp for emp in employees if emp.id == callback_data.employee_id), None)
        if employee:
            # Формируем текст с информацией о сотруднике
            text = (
                f"👤 *Имя:* {employee.username}\n\n"
                f"📝 *Описание:* {employee.description}\n\n"
                f"💼 *Должность:* {employee.role}\n\n"
                f"📞 *Телефон:* {employee.phone}\n\n"
                f"🔗 *Telegram:* {employee.telegram_username if employee.telegram_username else 'не указан'}"
            )

            await callback.message.edit_text(
                text=text,
                reply_markup=get_employee_edit_keyboard(employee_id=employee.id),
                parse_mode="HTML"
            )
        else:
            await callback.message.answer("Сотрудник не найден.")
    else:
        await callback.message.answer(f"Ошибка: {data_state.error_message}")


@router.callback_query(EmployeeCallback.filter(F.action == "delete"))
async def handle_delete_employee(callback: CallbackQuery, callback_data: EmployeeCallback):
    await callback.message.edit_text(
        text="Вы уверены, что хотите удалить этого сотрудника?",
        reply_markup=get_employee_delete_keyboard(employee_id=callback_data.employee_id)
    )

@router.callback_query(EmployeeCallback.filter(F.action == "confirm_delete"))
async def handle_confirm_delete(callback: CallbackQuery, callback_data: EmployeeCallback):
    # Удаляем сотрудника из базы данных
    data_state = KeyEmployeeDbBl.key_employee_delete(callback_data.employee_id)
    if isinstance(data_state, DataSuccess):
        admin_logger.info(
            f'Админ {CallbackQuery.message.chat.full_name} ({CallbackQuery.message.chat.id} удалил сотрудника)')
        await callback.message.edit_text(
            text="Сотрудник успешно удалён!",
            reply_markup=get_admin_main_keyboard()  # Возвращаем меню с действиями
        )
    else:
        await callback.message.edit_text(f"Ошибка: {data_state.error_message}")
