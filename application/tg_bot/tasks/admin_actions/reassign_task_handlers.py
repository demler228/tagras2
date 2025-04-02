from datetime import datetime
from loguru import logger
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram import Router, F, types
from domain.tasks.db_bl import TasksDbBl
from utils.data_state import DataSuccess

from .keyboards import (

    skip_keyboard,
    update_task_actions, task_action_keyboard, back_to_tasks_list, build_user_selection_keyboard
)
from .keyboards.callback_factories import TaskActionCallbackFactory, UpdateActionCallbackFactory

router = Router()


@router.callback_query(F.data == "reassign_task")
async def handle_reassign_task(callback_query: types.CallbackQuery, state: FSMContext):
    try:
        logger.info(f"handle_reassign_task is handled")
        state_data = await state.get_data()
        task_id = state_data.get("task_id")

        all_users_data_state = TasksDbBl.get_all_users()

        if not isinstance(all_users_data_state, DataSuccess) or not all_users_data_state.data:
            await callback_query.answer("Не удалось получить список всех пользователей", show_alert=True)
            return

        all_users = all_users_data_state.data

        assigned_users_data_state = TasksDbBl.get_assigned_users_by_task_id(task_id)
        if not isinstance(assigned_users_data_state, DataSuccess) or not assigned_users_data_state.data:
            await callback_query.answer("Не удалось получить список присвоенных пользователей", show_alert=True)
            return

        assigned_users = assigned_users_data_state.data
        selected_users = []
        for user in assigned_users:
            selected_users.append(user.id)

        await callback_query.message.edit_reply_markup(
            reply_markup=build_user_selection_keyboard(all_users=all_users,
                                                       selected_users=selected_users,
                                                       task_id=task_id))

    except Exception as e:
        logger.error(f"Ошибка в handle_reassign_task: {e}")
        await callback_query.message.answer("Произошла ошибка при обработке запроса.")
