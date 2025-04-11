from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from loguru import logger
from application.tg_bot.filters.is_admin import IsAdminFilter
from domain.tasks.db_bl import TasksDbBl
from application.tg_bot.filters.is_admin import is_super_admin
from application.tg_bot.menu.admin_actions.keyboards.menu_keyboard import get_admin_main_menu_keyboard
from utils.data_state import DataSuccess

router = Router()


@router.callback_query(F.data == "redefining_roles_super_admin")
async def redefining_roles_handler(callback_query: types.CallbackQuery):
    data_state = TasksDbBl.get_all_users()
    logger.info(f"redefining_roles_handler is handled")
    users_list = f"Список пользаветелей:\n\n"

    if isinstance(data_state, DataSuccess) and data_state.data:
        users = data_state.data
        for idx, user in enumerate(users, start=1):
            users_list += f"{idx}. {user.username} - [{user.role}]\n"

        await callback_query.message.answer(text=users_list)
    else:
        await callback_query.message.answer("Задачи не найдены")
