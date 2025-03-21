from aiogram import Router, F, types
from domain.tasks.db_bl import TasksDbBl
from .keyboards import get_tasks_keyboard

router = Router()


@router.callback_query(F.data == "tasks_button")
async def handle_tasks_button(callback_query: types.CallbackQuery):
    user_tg_id = callback_query.from_user.id

    tasks = TasksDbBl.get_tasks()

    await callback_query.message.answer("Вот ваш список задач:", reply_markup=get_tasks_keyboard())
