from aiogram import Router, F, types
from domain.tasks.db_bl import TasksDbBl
from utils.data_state import DataSuccess
from .keyboards import get_tasks_for_user_keyboard, back_to_tasks_list
from .keyboards import TaskCallbackFactory, BackTasksListCallbackFactory

router = Router()


@router.callback_query(F.data == "tasks_button")
async def handle_tasks_button(callback_query: types.CallbackQuery):
    user_tg_id = callback_query.from_user.id

    await callback_query.message.answer(
        "Вот ваш список задач:",
        reply_markup=get_tasks_for_user_keyboard(user_tg_id)
    )


@router.callback_query(TaskCallbackFactory.filter())
async def handle_task_description_button(callback_query: types.CallbackQuery, callback_data: TaskCallbackFactory):
    task_id = callback_data.task_id
    user_tg_id = callback_query.from_user.id
    data_state = TasksDbBl.get_tasks_by_tg_id(user_tg_id)
    if isinstance(data_state, DataSuccess):
        tasks = data_state.data

        task = next((t for t in tasks if t.id == task_id), None)

        if task:

            message = (
                f"<b>Задача:</b> {task.name}\n\n"
                f"<b>Описание:</b> {task.description if task.description else 'Нет описания'}\n\n"
                f"<b>Дата создания:</b> {task.creation_date.strftime('%Y-%m-%d')}\n\n"
                f"<b>Дедлайн:</b> {task.deadline.strftime('%Y-%m-%d') if task.deadline else 'Не указан'}"
            )
            await callback_query.message.edit_text(message, parse_mode="HTML", reply_markup=back_to_tasks_list())
        else:
            await callback_query.message.edit_text(f"Ошибка в получении данных задачи")
    else:
        await callback_query.message.edit_text(f"Ошибка в получении списка задач")


@router.callback_query(BackTasksListCallbackFactory.filter())
async def back_to_tasks_list_handler(callback_query: types.CallbackQuery):
    user_tg_id = callback_query.from_user.id

    await callback_query.message.edit_text(
        "Вот ваш список задач:",
        reply_markup=get_tasks_for_user_keyboard(user_tg_id)
    )
