from aiogram import Router, types, F
from application.tg_bot.faq.admin_actions.keyboards.faq_keyboard import get_faq_keyboard
from utils.container import faq_db_bl
from utils.data_state import DataSuccess

router = Router()

@router.callback_query(F.data == "faq_button_admin")
async def handle_faq_button(callback_query: types.CallbackQuery):
    await callback_query.message.delete()
    data_state = faq_db_bl.get_faq_list()
    if isinstance(data_state, DataSuccess):
        await callback_query.message.answer("📖 Ответы на частые вопросы",reply_markup=get_faq_keyboard(data_state.data))
    else:
        await callback_query.message.answer(f'❌ {data_state.error_message}')

@router.callback_query(F.data.contains("faq_question_button"))
async def handle_faq_button(callback_query: types.CallbackQuery):
    id = callback_query.data.split('-')[-1]
    #faq_list = faq_db_bl.get_faq_list()
    #await callback_query.message.answer("📖 Ответы на частые вопросы",reply_markup=get_faq_keyboard(faq_list))