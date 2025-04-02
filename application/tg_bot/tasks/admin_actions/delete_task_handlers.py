from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram import Router, F, types

from domain.tasks.db_bl import TasksDbBl

from .keyboards.callback_factories import (TaskAdminCallbackFactory)

from utils.data_state import DataSuccess

from .keyboards import task_admin_panel_keyboard, menu_of_action_after_creating, get_all_tasks_button

class DeleteTaskState(StatesGroup):
    delete_task: State()
    task_id: State()


router = Router()

@router.callback_query(F.data == "delete_task")
async def start_delete_task(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(DeleteTaskState.delete_task)
    await callback_query.message.answer(
        "Полный список задач:",
        reply_markup=get_all_tasks_button()
    )



@router.callback_query(TaskAdminCallbackFactory.filter())
async def handle_task_info(
        callback_query: types.CallbackQuery,
        callback_data: TaskAdminCallbackFactory,
        state: FSMContext
        
):
    task_id = callback_data.task_id
    await state.update_data(task_id=task_id)

    data_state = TasksDbBl.get_task_detail_by_task_id(task_id)

    if isinstance(data_state, DataSuccess) and data_state.data:
        task = data_state.data

        message = (
            f"<b>Задача:</b> {task.name}\n\n"
            f"<b>Описание:</b> {task.description if task.description else 'Нет описания'}\n\n"
            f"<b>Дата создания:</b> {task.creation_date.strftime('%Y-%m-%d')}\n\n"
            f"<b>Дедлайн:</b> {task.deadline.strftime('%Y-%m-%d') if task.deadline else 'Не указан'}"
        )

        await callback_query.message.edit_text(
            message,
            parse_mode="HTML",
            reply_markup=menu_of_action_after_creating()
        )
    else:
        await callback_query.message.edit_text("Задача не найдена")

