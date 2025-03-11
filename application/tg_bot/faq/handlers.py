from aiogram import Router, types, F

router = Router()

@router.callback_query(F.data == "faq_button")
async def handle_faq_button(callback_query: types.CallbackQuery):
    await callback_query.message.answer("Тут будет FAQ")