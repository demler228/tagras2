from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram.exceptions import TelegramBadRequest

from .keyboards.callback_factories import AdminActionCallback
from .keyboards.keyboards import get_admin_menu_keyboard

router = Router()


@router.callback_query(F.data == "department_list_button_admin")
async def handle_admin_menu(callback_query: CallbackQuery):
    """
    Обрабатывает нажатие на кнопку для вызова админ-меню.
    """
    try:
        # Отправляем меню с выбором действия
        await callback_query.message.edit_text(
            text="Выберите действие с отделами и пользователями:",
            reply_markup=get_admin_menu_keyboard(),
        )
    except TelegramBadRequest as e:
        await callback_query.answer("Невозможно обновить сообщение")


@router.callback_query(AdminActionCallback.filter())
async def handle_admin_action(
    callback_query: CallbackQuery, callback_data: AdminActionCallback
):
    """
    Обрабатывает выбор действия в админ-меню.
    """
    action = callback_data.action

    if action == "view_departments":
        # Здесь будет логика для просмотра отделов
        await callback_query.message.edit_text(
            "Список отделов (представление данных)..."
        )

    elif action == "add_department":
        # Здесь будет логика для добавления отдела
        await callback_query.message.edit_text("Форма для добавления отдела...")

    elif action == "edit_department":
        # Здесь будет логика для изменения отдела
        await callback_query.message.edit_text("Форма для изменения отдела...")

    elif action == "delete_department":
        # Здесь будет логика для удаления отдела
        await callback_query.message.edit_text("Форма для удаления отдела...")

    elif action == "view_employees":
        # Здесь будет логика для просмотра сотрудников
        await callback_query.message.edit_text(
            "Список сотрудников (представление данных)..."
        )

    elif action == "add_employee":
        # Здесь будет логика для добавления сотрудника
        await callback_query.message.edit_text("Форма для добавления сотрудника...")

    elif action == "edit_employee":
        # Здесь будет логика для изменения сотрудника
        await callback_query.message.edit_text("Форма для изменения сотрудника...")

    elif action == "delete_employee":
        # Здесь будет логика для удаления сотрудника
        await callback_query.message.edit_text("Форма для удаления сотрудника...")
