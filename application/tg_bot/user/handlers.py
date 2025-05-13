from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from application.tg_bot.menu.admin_actions.keyboards.menu_keyboard import get_admin_main_menu_keyboard
from application.tg_bot.user.keyboards.get_confirm_edit_buttons import get_confirm_edit_keyboard, \
    get_edit_options_keyboard, get_back_employee_button
from application.tg_bot.user.keyboards.get_employee_menu_keyboard import get_employee_menu_keyboard
from application.tg_bot.user.entities.user import User
from domain.user.bl_models.db_bl import UserBL
from application.tg_bot.user.keyboards.get_confirm_edit_buttons import get_employee_action_keyboard
from application.tg_bot.user.keyboards.get_confirm_edit_buttons import EmployeeCallback
from utils.data_state import DataSuccess, DataFailedMessage
from application.tg_bot.user.keyboards.get_confirm_edit_buttons import get_employee_list_keyboard

router = Router()

class EmployeeStates(StatesGroup):
    add_employee_name = State()
    add_employee_phone = State()
    add_employee_tg_username = State()
    add_employee_telegram_id = State()

    edit_employee_name = State()
    edit_employee_phone = State()
    edit_employee_tg_username = State()
    edit_employee_telegram_id = State()

@router.callback_query(F.data == "employees_button_admin")
async def employee_handler(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(
        "Меню для работы с сотрудниками.\nПожалуйста, выберите дальнейшее действие:",
        reply_markup=get_employee_menu_keyboard()
    )

@router.callback_query(F.data == "employee_create_admin_button")
async def add_user_handler(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(EmployeeStates.add_employee_name)
    await callback_query.message.answer("✍️ Введите имя и фамилию сотрудника",
                                        reply_markup=get_back_employee_button())

@router.message(EmployeeStates.add_employee_name)
async def add_user_name_handler(message: types.Message, state: FSMContext):
    await state.update_data({"username": message.text})
    await state.set_state(EmployeeStates.add_employee_phone)
    await message.answer("✍️ Введите номер телефона сотрудника",
                         reply_markup=get_back_employee_button())

@router.message(EmployeeStates.add_employee_phone)
async def add_user_phone_handler(message: types.Message, state: FSMContext):
    await state.update_data({"phone": message.text})
    await state.set_state(EmployeeStates.add_employee_tg_username)
    await message.answer("✍️ Введите username сотрудника в Telegram \n(формат - @username)",
                         reply_markup=get_back_employee_button())

@router.message(EmployeeStates.add_employee_tg_username)
async def add_user_tg_username_handler(message: types.Message, state: FSMContext):
    await state.update_data({"tg_username": message.text})
    await state.set_state(EmployeeStates.add_employee_telegram_id)
    await message.answer("✍️ Введите Telegram ID сотрудника \n(формат - числовой ID, например 123456789)",
                         reply_markup=get_back_employee_button())

@router.message(EmployeeStates.add_employee_telegram_id)
async def add_telegram_id_handler(message: types.Message, state: FSMContext):
    await state.update_data({"telegram_id": message.text})
    await show_confirm_screen(message, state)

@router.callback_query(F.data == "employee_edit")
async def employee_edit_handler(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(
        "Что вы хотите отредактировать?",
        reply_markup=get_edit_options_keyboard()
    )

@router.callback_query(F.data == "edit_employee_name")
async def edit_name(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(EmployeeStates.edit_employee_name)
    await callback_query.message.answer("✍️ Введите новое имя и фамилию сотрудника",
                                        reply_markup=get_back_employee_button())

@router.callback_query(F.data == "edit_employee_phone")
async def edit_phone(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(EmployeeStates.edit_employee_phone)
    await callback_query.message.answer("✍️ Введите новый номер телефона сотрудника",
                                        reply_markup=get_back_employee_button())

@router.callback_query(F.data == "edit_employee_username")
async def edit_tg_username(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(EmployeeStates.edit_employee_tg_username)
    await callback_query.message.answer("✍️ Введите новый username сотрудника в Telegram \n(формат - @username)",
                                        reply_markup=get_back_employee_button())

@router.callback_query(F.data == "edit_employee_telegram_id")
async def edit_tg_username(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(EmployeeStates.edit_employee_telegram_id)
    await callback_query.message.answer("✍️ Введите новый Telegram ID сотрудника \n(формат - числовой ID, например 123456789)",
                                        reply_markup=get_back_employee_button())

@router.message(EmployeeStates.edit_employee_name)
async def edited_name_handler(message: types.Message, state: FSMContext):
    await state.update_data({"username": message.text})
    await show_confirm_screen(message, state)

@router.message(EmployeeStates.edit_employee_phone)
async def edited_phone_handler(message: types.Message, state: FSMContext):
    await state.update_data({"phone": message.text})
    await show_confirm_screen(message, state)

@router.message(EmployeeStates.edit_employee_tg_username)
async def edited_telegram_id_handler(message: types.Message, state: FSMContext):
    await state.update_data({"tg_username": message.text})
    await show_confirm_screen(message, state)

@router.message(EmployeeStates.edit_employee_telegram_id)
async def edited_telegram_id_handler(message: types.Message, state: FSMContext):
    await state.update_data({"telegram_id": message.text})
    await show_confirm_screen(message, state)

async def show_confirm_screen(message_or_query: types.Message | types.CallbackQuery, state: FSMContext):
    data = await state.get_data()

    user = User(
        username=data["username"],
        phone=data["phone"],
        tg_username=data["tg_username"],
        telegram_id = data["telegram_id"]
    )

    text = (
        f"🔎 Проверьте введённые данные:\n\n"
        f"👤 Полное имя: {user.username}\n"
        f"📞 Телефон: {user.phone}\n"
        f"📱 Telegram username: {user.tg_username}\n"
        f"🔢 Telegram telegram id: {user.telegram_id}"
    )
    if isinstance(message_or_query, types.CallbackQuery):
        await message_or_query.message.edit_text(text, reply_markup=get_confirm_edit_keyboard())
    else:
        await message_or_query.answer(text, reply_markup=get_confirm_edit_keyboard())

@router.callback_query(F.data == "employee_save")
async def save_employee_handler(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()

    if "employee_id" in data:
        employee_id = data["employee_id"]
        updates = {
            "username": data["username"],
            "phone": data["phone"],
            "tg_username": data["tg_username"],
            "telegram_id": data["telegram_id"]
        }
        data_state = UserBL.update_employee(employee_id, updates)
        if isinstance(data_state, DataSuccess):
            await callback_query.message.edit_text(
                f"✅ Сотрудник успешно обновлён:\n"
                f"👤 {data['username']}\n📞 {data['phone']}\n📱 {data['tg_username']}",
                reply_markup=get_back_employee_button()
            )
        else:
            await callback_query.message.edit_text(
                "Не удалось обновить данные сотрудника\n",
                reply_markup=get_back_employee_button()
            )
    else:
        user = User(
            username=data["username"],
            phone=data["phone"],
            tg_username=data["tg_username"],
            telegram_id=data["telegram_id"]
        )
        data_state = await UserBL.add_employee(user)
        if isinstance(data_state, DataSuccess):
            await callback_query.message.edit_text(
                f"✅ Сотрудник успешно сохранён:\n"
                f"👤 {user.username}\n📞 {user.phone}\n📱 {user.tg_username}",
                reply_markup=get_back_employee_button()
            )
        else:
            await callback_query.message.edit_text(
                "Не удалось добавить сотрудника\n",
                reply_markup=get_back_employee_button()
            )
    await state.clear()

@router.callback_query(F.data == "get_admin_main_menu")
async def get_main_menu_handler(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(
        "Вы вернулись в главное меню.",
        reply_markup=get_admin_main_menu_keyboard()
    )

@router.callback_query(F.data == "confirm_data_employee_back")
async def confirm_data_back_handler(callback_query: types.CallbackQuery, state: FSMContext):
    await show_confirm_screen(callback_query, state)

@router.callback_query(F.data == "employee_back_button")
async def back_employee_handler(callback_query: types.CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state in [
        EmployeeStates.edit_employee_name.state,
        EmployeeStates.edit_employee_phone.state,
        EmployeeStates.edit_employee_tg_username.state
    ]:
        await callback_query.message.edit_text(
            "Вы вернулись в меню редактирования сотрудника.",
            reply_markup=get_edit_options_keyboard()
        )
    else:
        await callback_query.message.edit_text(
            "Меню для работы с сотрудниками.\nПожалуйста, выберите дальнейшее действие:",
            reply_markup=get_employee_menu_keyboard()
        )

@router.callback_query(F.data == "get_employees_list_button")
async def list_employees_handler(callback_query: types.CallbackQuery):
    data_state = UserBL.get_all_employees()
    if isinstance(data_state, DataFailedMessage):
        await callback_query.message.edit_text(
            f"Ошибка: {data_state.error_message}",
            reply_markup=get_back_employee_button()
        )
        return
    employees = data_state.data
    if not employees:
        await callback_query.message.edit_text(
            "Список сотрудников пуст.",
            reply_markup=get_back_employee_button()
        )
        return
    await callback_query.message.edit_text(
        "👥 Выберите сотрудника для редактирования:",
        reply_markup=get_employee_list_keyboard(employees)
    )

@router.callback_query(EmployeeCallback.filter(F.action == "view"))
async def view_employee_handler(callback_query: types.CallbackQuery, callback_data: EmployeeCallback):
    employee_id = callback_data.employee_id
    data_state = UserBL.get_employee_by_id(employee_id)
    if isinstance(data_state, DataFailedMessage):
        await callback_query.message.edit_text(
            f"Ошибка: {data_state.error_message}",
            reply_markup=get_back_employee_button()
        )
        return
    employee = data_state.data
    await callback_query.message.edit_text(
        f"Информация о сотруднике:\n\n"
        f"👤 Имя: {employee.username}\n"
        f"📞 Телефон: {employee.phone}\n"
        f"📱 Telegram: {employee.tg_username}\n"
        f"🔑 Роль: {employee.role}",
        reply_markup=get_employee_action_keyboard(employee.id)
    )

@router.callback_query(EmployeeCallback.filter(F.action == "edit"))
async def edit_employee_handler(callback_query: types.CallbackQuery, callback_data: EmployeeCallback,
                                state: FSMContext):
    employee_id = callback_data.employee_id
    data_state = UserBL.get_employee_by_id(employee_id)
    if isinstance(data_state, DataFailedMessage):
        await callback_query.message.edit_text(
            f"Ошибка: {data_state.error_message}",
            reply_markup=get_back_employee_button()
        )
        return
    employee = data_state.data

    await state.update_data({
        "employee_id": employee.id,
        "username": employee.username,
        "phone": employee.phone,
        "tg_username": employee.tg_username,
        "telegram_id": employee.telegram_id
    })
    await callback_query.message.edit_text(
        "Что вы хотите отредактировать?",
        reply_markup=get_edit_options_keyboard()
    )

@router.callback_query(EmployeeCallback.filter(F.action == "delete"))
async def delete_employee_handler(callback_query: types.CallbackQuery, callback_data: EmployeeCallback):
    employee_id = callback_data.employee_id
    data_state = UserBL.delete_employee(employee_id)
    if isinstance(data_state, DataSuccess):
        await callback_query.message.edit_text(
            "✅ Сотрудник успешно удалён.",
            reply_markup=get_employee_list_keyboard([])
        )
    else:
        await callback_query.message.edit_text(
            f"❌ Не удалось удалить сотрудника: {data_state.error_message}",
            reply_markup=get_back_employee_button()
        )
