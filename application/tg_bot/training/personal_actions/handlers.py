from aiogram import Router, types, F

from .training_menu_keyboard import get_training_menu_keyboard


router = Router()

@router.callback_query(F.data == "training_button")
async def handle_training_button(callback_query: types.CallbackQuery):
    await  callback_query.message.answer("Выбери 1 из вариантов и нажми на нее:", reply_markup=get_training_menu_keyboard())