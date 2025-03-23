from aiogram import Router, F
from aiogram.types import CallbackQuery

router = Router()

@router.callback_query(F.data == "department_list_button")
async def handle_contacts_button(callback_query: CallbackQuery):
    await callback_query.message.answer(text="Тут скоро появится список разделов")