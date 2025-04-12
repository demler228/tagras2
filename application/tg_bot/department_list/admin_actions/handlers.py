from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

from domain.department_list.db_bl import DepartmentDbBl, EmployeeDbBl
from sympy.printing.precedence import precedence_Integer

from ..entities.department_list import Department, Employee
from utils.data_state import DataSuccess
from .keyboards.department_keyboard import (
    get_department_list_keyboard,
    get_department_employee_list_keyboard,
    get_department_employee_detail_keyboard,
    get_confirm_delete_keyboard,
    get_employee_edit_fields_keyboard,
    get_cancel_keyboard,
    back_to_dept,
    back_to_employees,
    back_to_employee_view
)
from .keyboards.callback_factories import (
    AdminDepartmentCallback,
    AdminDepartmentListCallback,
    AdminDepartmentEmployeeCallback,
    AdminDepartmentEmployeePageCallback,
    AdminConfirmCallback,
    AdminEmployeeEditFieldCallback,
)

from aiogram.fsm.state import State, StatesGroup

router = Router()


# ==== FSM Состояния ====
class AddDepartmentState(StatesGroup):
    name = State()


class AddEmployeeState(StatesGroup):
    name = State()
    phone = State()
    description = State()


class EditEmployeeState(StatesGroup):
    field = State()
    value = State()


# ======= ОБРАБОТЧИКИ СПИСКА ОТДЕЛОВ =======


@router.callback_query(F.data == "department_list_button_admin")
@router.callback_query(F.data.startswith("admin_departments_page:"))
async def handle_admin_department_list(callback_query: CallbackQuery):
    if callback_query.data == "department_list_button_admin":
        page = 1
    else:
        callback_data = AdminDepartmentListCallback.unpack(callback_query.data)
        page = callback_data.page
    departments_state = DepartmentDbBl.get_department_list()
    if not isinstance(departments_state, DataSuccess):
        await callback_query.answer("Ошибка загрузки отделов")
        return
    departments = departments_state.data

    await callback_query.message.edit_text(
        text="📋 Список отделов:",
        reply_markup=get_department_list_keyboard(departments, page, admin=True),
    )


# ======= ОБРАБОТЧИК ОТДЕЛА =======


@router.callback_query(AdminDepartmentCallback.filter(F.action == "view"))
@router.callback_query(AdminDepartmentEmployeePageCallback.filter())
async def handle_admin_department_view(callback: CallbackQuery, callback_data):
    department_id = callback_data.department_id
    page = getattr(callback_data, "page", 1)
    employees_state = EmployeeDbBl.get_employee_list(department_id)
    if not isinstance(employees_state, DataSuccess):
        await callback.answer("Ошибка загрузки сотрудников")
        return
    employees = employees_state.data

    await callback.message.edit_text(
        text="👥 Сотрудники отдела:",
        reply_markup=get_department_employee_list_keyboard(
            employees, department_id, page, admin=True
        ),
    )


@router.callback_query(F.data == "add_department_button")
async def handle_add_department_start(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AddDepartmentState.name)
    await callback.message.edit_text(
        text="Введите название нового отдела:", reply_markup=get_cancel_keyboard()
    )


@router.message(AddDepartmentState.name, F.text)
async def process_add_department_name(message: Message, state: FSMContext):
    name = message.text.strip()
    if not name:
        await message.answer("Название отдела не может быть пустым. Введите название:")
        return

    department = Department(name=name)
    result = DepartmentDbBl.create_department(department)
    if isinstance(result, DataSuccess):
        await message.answer(
            text=f"✅ Отдел '{name}' успешно создан!", reply_markup=back_to_dept()
        )
    else:
        await message.answer(
            text=f"❌ Ошибка при создании отдела: {result.message}",
            reply_markup=back_to_dept(),
        )
    await state.clear()


# ======= ДОБАВЛЕНИЕ СОТРУДНИКА =======


@router.callback_query(AdminDepartmentCallback.filter(F.action == "add_employee"))
async def handle_add_employee_start(
    callback: CallbackQuery, callback_data: AdminDepartmentCallback, state: FSMContext
):
    """Начало добавления сотрудника - запрос имени"""
    await state.update_data(department_id=callback_data.department_id)
    await state.set_state(AddEmployeeState.name)
    await callback.message.edit_text(
        "Введите имя сотрудника (обязательно):",
        reply_markup=get_cancel_keyboard("department_list_button_admin"),
    )


@router.message(AddEmployeeState.name, F.text)
async def process_employee_name(message: Message, state: FSMContext):
    """Обработка имени сотрудника"""
    name = message.text.strip()
    if not name:
        await message.answer("Имя не может быть пустым. Введите имя:")
        return

    await state.update_data(name=name)
    await state.set_state(AddEmployeeState.phone)
    await message.answer(
        "Введите телефон сотрудника (или '-', если не указан):",
        reply_markup=get_cancel_keyboard("department_list_button_admin"),
    )


@router.message(AddEmployeeState.phone, F.text)
async def process_employee_phone(message: Message, state: FSMContext):
    """Обработка телефона сотрудника"""
    phone = message.text.strip()
    phone = None if phone == "-" else phone
    await state.update_data(phone=phone)
    await state.set_state(AddEmployeeState.description)
    await message.answer(
        "Введите описание сотрудника (или '-', если не указано):",
        reply_markup=get_cancel_keyboard("department_list_button_admin"),
    )


@router.message(AddEmployeeState.description, F.text)
async def process_employee_description(message: Message, state: FSMContext):
    """Финальная обработка и сохранение сотрудника"""
    description = message.text.strip()
    description = None if description == "-" else description

    data = await state.get_data()
    # Создаем объект сотрудника
    employee = Employee(
        name=data["name"],
        phone=data.get("phone"),
        description=description,
        department_id=data["department_id"],
    )
    # Сохраняем в БД
    result = EmployeeDbBl.create_employee(employee)

    if isinstance(result, DataSuccess):
        await message.answer(
            text="✅ Сотрудник успешно добавлен!",
            reply_markup=back_to_employees(data["department_id"]),
        )
    else:
        await message.answer(
            text=f"❌ Ошибка при добавлении: {result.message}",
            reply_markup=back_to_employees(data["department_id"]),
        )

    await state.clear()


# ======= УДАЛЕНИЕ ОТДЕЛА =======


@router.callback_query(AdminDepartmentCallback.filter(F.action == "delete"))
async def handle_delete_department(
    callback: CallbackQuery, callback_data: AdminDepartmentCallback
):
    """Показать подтверждение удаления отдела"""
    await callback.message.edit_text(
        text="⚠️ Вы уверены, что хотите удалить отдел и всех его сотрудников?",
        reply_markup=get_confirm_delete_keyboard(
            entity_id=callback_data.department_id, target="department"
        ),
    )


@router.callback_query(AdminConfirmCallback.filter(F.target == "department"))
async def confirm_delete_department(
    callback: CallbackQuery, callback_data: AdminConfirmCallback
):
    """Обработка подтверждения удаления"""
    department_id = callback_data.entity_id
    # Получаем название отдела для сообщения
    dept_state = DepartmentDbBl.get_department_details(department_id)
    if not isinstance(dept_state, DataSuccess):
        await callback.answer("Ошибка: отдел не найден")
        return
    result = DepartmentDbBl.delete_department(department_id)
    if isinstance(result, DataSuccess):
        await callback.message.edit_text(
            text=f"✅ Отдел '{dept_state.data.name}' и все его сотрудники удалены",
            reply_markup=back_to_dept(),
        )
    else:
        await callback.message.edit_text(
            text=f"❌ Ошибка при удалении: {result.message}\n\n",
            reply_markup=back_to_dept(),
        )


# ======= ПРОСМОТР ИНФО О СОТРУДНИКЕ =======


@router.callback_query(AdminDepartmentEmployeeCallback.filter(F.action == "view"))
async def handle_view_employee(
    callback: CallbackQuery, callback_data: AdminDepartmentEmployeeCallback
):
    employee_state = EmployeeDbBl.get_employee_details(callback_data.employee_id)
    if not isinstance(employee_state, DataSuccess):
        await callback.message.edit_text("❌ Ошибка при получении данных сотрудника")
        return

    employee = employee_state.data
    await callback.message.edit_text(
        text=(
            f"👤 {employee.name}\n"
            f"📞 Телефон: {employee.phone or 'нет телефона'}\n"
            f"📝 Описание: {employee.description or 'нет описания'}"
        ),
        reply_markup=get_department_employee_detail_keyboard(
            employee.id, employee.department_id, admin=True
        ),
    )


# ======= УДАЛЕНИЕ СОТРУДНИКА =======


@router.callback_query(AdminDepartmentEmployeeCallback.filter(F.action == "delete"))
async def handle_delete_employee_request(
    callback: CallbackQuery, callback_data: AdminDepartmentEmployeeCallback
):
    """Запрос подтверждения удаления сотрудника"""
    employee_state = EmployeeDbBl.get_employee_details(callback_data.employee_id)

    if not isinstance(employee_state, DataSuccess):
        await callback.answer("Сотрудник не найден")
        return

    employee = employee_state.data

    await callback.message.edit_text(
        text=f"⚠️ Вы уверены, что хотите удалить сотрудника {employee.name}?",
        reply_markup=get_confirm_delete_keyboard(
            entity_id=callback_data.employee_id, target="employee"
        ),
    )


@router.callback_query(AdminConfirmCallback.filter(F.target == "employee"))
async def handle_confirm_delete_employee(
    callback: CallbackQuery, callback_data: AdminConfirmCallback
):
    """Обработка подтверждения удаления сотрудника"""
    # Получаем данные сотрудника для сообщения
    employee_state = EmployeeDbBl.get_employee_details(callback_data.entity_id)

    if not isinstance(employee_state, DataSuccess):
        await callback.answer("Сотрудник не найден")
        return

    employee = employee_state.data

    # Удаляем сотрудника
    result = EmployeeDbBl.delete_employee(callback_data.entity_id)
    if isinstance(result, DataSuccess):
        await callback.message.edit_text(
            text=f"✅ Сотрудник {employee.name} успешно удалён",
            reply_markup=back_to_employees(employee.department_id),
        )
    else:
        await callback.answer(
            text=f"Ошибка: {result.message}",
            show_alert=True
        )


# ======= ИЗМЕНЕНИЕ СОТРУДНИКА =======


@router.callback_query(AdminDepartmentEmployeeCallback.filter(F.action == "edit"))
async def handle_edit_employee_start(
        callback: CallbackQuery,
        callback_data: AdminDepartmentEmployeeCallback
):
    """Начало редактирования - выбор поля"""
    await callback.message.edit_text(
        text="Выберите поле для редактирования:",
        reply_markup=get_employee_edit_fields_keyboard(callback_data.employee_id)
    )


@router.callback_query(AdminEmployeeEditFieldCallback.filter())
async def handle_choose_edit_field(
        callback: CallbackQuery,
        callback_data: AdminEmployeeEditFieldCallback,
        state: FSMContext
):
    """Обработка выбора поля для редактирования"""
    await state.update_data(
        employee_id=callback_data.employee_id,
        field=callback_data.field
    )

    field_descriptions = {
        "name": "имя (обязательное поле, нельзя очистить)",
        "phone": "телефона (введите '-', чтобы очистить)",
        "description": "описания (введите '-', чтобы очистить)"
    }

    await state.set_state(EditEmployeeState.value)
    await callback.message.edit_text(
        text=f"Введите новое значение для {field_descriptions[callback_data.field]}:",
        reply_markup=get_cancel_keyboard(
            AdminDepartmentEmployeeCallback(
                action="view",
                employee_id=callback_data.employee_id
            ).pack()
        )
    )


@router.message(EditEmployeeState.value, F.text)
async def handle_edit_field_value(
        message: Message,
        state: FSMContext
):
    """Обработка нового значения поля"""
    data = await state.get_data()
    field = data["field"]
    employee_id = data["employee_id"]
    value = message.text.strip()

    # Специальная обработка для разных полей
    if field == "name":
        if not value or value == "-":
            await message.answer("❌ Имя не может быть пустым. Введите снова:")
            return
    else:  # phone или description
        value = None if value == "-" else value

    # Обновляем поле в БД
    result = EmployeeDbBl.update_employee_field(employee_id, field, value)

    if isinstance(result, DataSuccess):
        # Получаем обновленные данные сотрудника
        employee_state = EmployeeDbBl.get_employee_details(employee_id)
        if isinstance(employee_state, DataSuccess):
            employee = employee_state.data
            await message.answer(
                text=f"✅ Поле '{field}' успешно обновлено!",
                reply_markup=back_to_employee_view(employee.id, employee.department_id)
            )
    else:
        await message.answer(
            text=f"❌ Ошибка при обновлении: {result.message}",
            reply_markup=back_to_employee_view(employee_id, data.get("department_id"))
        )

    await state.clear()
