from aiogram import Router, F
from aiogram.types import CallbackQuery
from .keyboards import get_user_keyboard

router = Router()

@router.callback_query(F.data == "contacts_button")
async def handle_contacts_button(callback_query: CallbackQuery):
    await callback_query.message.edit_text(
        text="Выберите что хотите узнать:\n",
        reply_markup=get_user_keyboard()
    )