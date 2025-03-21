from aiogram import Router, F, types

router = Router()


@router.callback_query(F.data == "tasks_button")
async def handle_tasks_button(callback_query: types.CallbackQuery):
    await callback_query.message.answer("Вот ваш список задач:")
