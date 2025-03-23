from aiogram import Router, types, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models.gigachat import GigaChat

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
    await callback_query.message.answer("Привет, я бот компании Таграс. Чем могу вам помочь?")
    await callback_query.answer()

@router.message(F.text)
async def handle_text_message(message: Message, state: FSMContext):
    current_state = await state.get_state()

    if current_state == AIState.active:
        user_input = message.text
        msgs.append(HumanMessage(content=user_input))
        answer = giga(msgs)
        msgs.append(answer)
        await message.answer(f"{answer.content}")
    else:
        await message.answer("Режим общения с ИИ не активирован. Нажмите кнопку, чтобы начать.")

@router.message(F.text.lower() == "выход")
async def handle_exit(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Режим общения с ИИ деактивирован.")