from aiogram import Router, types, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models.gigachat import GigaChat

from application.tg_bot.ai_assistant.keyboards.get_exit_button import get_exit_button_ai
from application.tg_bot.filters.is_admin import is_admin
from application.tg_bot.menu.personal_actions.keyboards.menu_keyboard import get_main_menu_keyboard

auth = "Y2U3ZDc2ODAtNGJmNy00ZmYzLWIxNzItM2JlMzc5NGFhNWI4OjMzOGMzY2ZkLTEwMzgtNGQyYi05ZTI3LTVhZjNhM2Q3ZjcyOA=="

giga = GigaChat(
    credentials=auth,
    model='GigaChat:latest',
    verify_ssl_certs=False
)

msgs = [
    SystemMessage(content='Ты являешься ии-помощником в компании "Таграс" и ты помогаешь отвечать на вопросы новым сотрудникам. \
                  Соответственно твои знания и миропонимание ограничены этим \
                  персонажем и его апатичной манерой поведения. Ты не можешь отвечать \
                  правильно на вопросы, на которые не может знать твой персонаж.')
]

class AIState(StatesGroup):
    active = State()

router = Router()

@router.callback_query(F.data == "ai_assistant_button")
async def handle_ai_assistant_button(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(AIState.active)
    await callback_query.message.edit_text("Привет, я бот компании Таграс. Чем могу вам помочь?")

@router.message(F.text, AIState.active)
async def handle_text_message(message: Message, state: FSMContext):
    user_input = message.text

    if user_input == "Вернуться в меню":
        await message.answer("Режим общения с ИИ деактивирован.\n\nДобро поаловать в меню",
                             reply_markup=get_main_menu_keyboard(is_admin(message.from_user.id)))
        return

    msgs.append(HumanMessage(content=user_input))
    answer = giga(msgs)
    msgs.append(answer)
    await message.answer(f"{answer.content}", reply_markup=get_exit_button_ai())
