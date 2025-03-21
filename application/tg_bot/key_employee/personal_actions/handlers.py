# application/tg_bot/key_employee/personal_actions/handlers.py
from aiogram import Router, F
from aiogram.types import CallbackQuery

router = Router()

@router.callback_query(F.data == "contacts_button")
async def handle_contacts_button(callback_query: CallbackQuery):
    await callback_query.message.answer(text="Тут очень скоро появится модуль полезные контакты")