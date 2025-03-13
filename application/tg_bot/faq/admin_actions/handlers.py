from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from application.tg_bot.faq.admin_actions.keyboards.faq_list_keyboard import get_faq_list_keyboard, FaqCallback
from application.tg_bot.faq.admin_actions.keyboards.faq_menu_keyboard import get_faq_menu_keyboard
from application.tg_bot.faq.entities.faq import Faq
from utils.container import faq_db_bl
from utils.data_state import DataSuccess

router = Router()
class AdminStates(StatesGroup):
    faq_menu = State()
    change_faq_question = State()
    change_faq_answer = State()

async def get_faq(state,callback_query=None, callback_data=None, message=None):
    await state.set_state(AdminStates.faq_menu)
    if message is None:
        await callback_query.message.delete()
        faq_list =  (await state.get_data())['faq_list']
        faq = next((faq for faq in faq_list if faq.id == callback_data.faq_id), None)
        message = await callback_query.message.answer(f"❓ <b>{faq.question}</b>\n\n☑️ {faq.answer}", reply_markup=get_faq_menu_keyboard(),parse_mode='HTML')

    else:
        # если вдруг еще кто-то изменяет этот вопрос-ответ, чтобы были актуальные данные
        data_state = faq_db_bl.get_faq_list()

        if isinstance(data_state, DataSuccess):
            faq_list = data_state.data
            changed_faq_id = (await state.get_data())['faq'].id
            faq = next((faq for faq in faq_list if faq.id == changed_faq_id), None)

            message = await message.answer(
                f"❓ <b>{faq.question}</b>\n\n☑️ {faq.answer}",
                reply_markup=get_faq_menu_keyboard(),parse_mode='HTML')
        else:
            await callback_query.message.answer(f'❌ {data_state.error_message}')
            return
    #стараемся минимизировать кол-во обращений к бд
    await state.set_data({'faq': faq, 'message': message})


@router.callback_query(F.data == "faq_button_admin")
async def handle_faq_list_button(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.delete()

    data_state = faq_db_bl.get_faq_list()
    if isinstance(data_state, DataSuccess):
        await state.set_data({'faq_list': data_state.data})
        await callback_query.message.answer("📖 Ответы на частые вопросы", reply_markup=get_faq_list_keyboard(data_state.data))
    else:
        await callback_query.message.answer(f'❌ {data_state.error_message}')


@router.callback_query(FaqCallback.filter())
async def handle_faq_button(callback_query: types.CallbackQuery, callback_data: FaqCallback, state: FSMContext):
    await get_faq(state, callback_query=callback_query,callback_data=callback_data)


@router.callback_query(F.data == "faq_change_question_button")
async def handle_faq_change_question_button(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(AdminStates.change_faq_question)
    await callback_query.message.answer(f"✍️ Введите новый вопрос")


@router.message(F.text, AdminStates.change_faq_question)
async def handle_faq_change_question_button(message: Message, state: FSMContext):
    faq = (await state.get_data())['faq']
    faq.question = message.text
    data_state = faq_db_bl.faq_update(faq)

    if isinstance(data_state, DataSuccess):
        await (await state.get_data())['message'].delete()
        await get_faq(state, message=message)
    else:
        await message.answer(f'❌ {data_state.error_message}')



@router.callback_query(F.data == "faq_change_answer_button")
async def handle_faq_change_question_button(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(AdminStates.change_faq_answer)
    await callback_query.message.answer(f"✍️ Введите новый ответ")


@router.message(F.text, AdminStates.change_faq_answer)
async def handle_faq_change_question_button(message: Message, state: FSMContext):
    faq = (await state.get_data())['faq']
    faq.answer = message.text
    data_state = faq_db_bl.faq_update(faq)

    if isinstance(data_state, DataSuccess):
        await (await state.get_data())['message'].delete()
        await get_faq(state, message=message)
    else:
        await message.answer(f'❌ {data_state.error_message}')

