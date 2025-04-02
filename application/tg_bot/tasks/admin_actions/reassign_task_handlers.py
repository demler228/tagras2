from datetime import datetime
from loguru import logger
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram import Router, F, types
from domain.tasks.db_bl import TasksDbBl
from utils.data_state import DataSuccess

from .keyboards import (

    skip_keyboard,
    update_task_actions, task_action_keyboard, back_to_tasks_list,
)
from .keyboards.callback_factories import TaskActionCallbackFactory, UpdateActionCallbackFactory

router = Router()

@router.callback_query(F.data == "reassign_task")
async def handle_reassign_task(callback_query: types.CallbackQuery, task_id: int):
    try:
        logger.info(f"Id of task: {task_id}")
        await callback_query.message.edit_text(text="Это переопределение пользователей", reply_markup=back_to_tasks_list())

    except Exception as e:
        logger.error(f"Ошибка в handle_reassign_task: {e}")
        await callback_query.message.answer("Произошла ошибка при обработке запроса.")
