from aiogram import Router, types, F
from aiogram.types import Message, CallbackQuery
from aiogram.enums import ParseMode
from domain.quiz.db_bl import DBService

from application.tg_bot.training.entities.questions import Question
from .keyboards import get_answers_keyboard, get_themes_keyboard
from .callback_factories import QuizCallbackFactory
from utils.data_state import DataSuccess
from application.tg_bot.menu.personal_actions.keyboards.menu_keyboard import get_main_menu_keyboard

router = Router()

user_data = {}


@router.callback_query(F.data == "quiz_button")
async def handle_quiz_button(callback_query: types.CallbackQuery):
    themes_result = DBService.get_themes()
    if isinstance(themes_result, DataSuccess):
        themes = themes_result.data
    else:
        await callback_query.message.answer("🚫 Темы для викторины не найдены.")
        return

    await callback_query.message.answer(
        "🎯 *Выберите тему для викторины:*",
        reply_markup=get_themes_keyboard(themes),
        parse_mode=ParseMode.MARKDOWN
    )
    await callback_query.answer()


@router.callback_query(QuizCallbackFactory.filter(F.action == "select_theme"))
async def handle_theme_selection(callback_query: CallbackQuery, callback_data: QuizCallbackFactory):
    theme_id = callback_data.theme_id
    user_id = callback_query.from_user.id

    questions_result = DBService.get_questions_by_theme(theme_id)
    if isinstance(questions_result, DataSuccess):
        questions = questions_result.data  # Список объектов Question
        print(f'questions - {questions}')
    else:
        await callback_query.message.answer("🚫 Вопросы по выбранной теме не найдены.")
        return

    if not questions:
        await callback_query.message.answer("🚫 Вопросы по выбранной теме не найдены.")
        return

    user_data[user_id] = {
        "step": "quiz_in_progress",
        "questions": questions,
        "current_question": 0,
        "score": 0,
        "message_id": None,
    }

    await send_question(callback_query.message, user_id)
    await callback_query.answer()

@router.callback_query(QuizCallbackFactory.filter(F.action == "answer"))
async def handle_answer_selection(callback_query: CallbackQuery, callback_data: QuizCallbackFactory):
    user_id = callback_query.from_user.id
    user_state = user_data.get(user_id, {})

    if user_state.get("step") != "quiz_in_progress":
        await callback_query.answer("🚫 Викторина не активна.")
        return

    selected_answer_index = callback_data.answer_index
    print(f'selected answer - {selected_answer_index}')
    questions = user_state["questions"]
    current_question_index = user_state["current_question"]
    current_question: Question = questions[current_question_index]

    correct_answer = current_question.correct_answer
    print(f'correct_answer - {correct_answer}')

    correct_answer_index = current_question.answers.index(correct_answer)
    print(f'correct_answer_index - {correct_answer_index}')

    if selected_answer_index == correct_answer_index:
        user_state["score"] += 1

    user_state["current_question"] += 1
    if user_state["current_question"] < len(questions):
        await send_question(callback_query.message, user_id)
    else:
        score = user_state["score"]
        total_questions = len(questions)

        await callback_query.message.bot.delete_message(
            chat_id=callback_query.message.chat.id,
            message_id=user_state["message_id"]
        )

        await callback_query.message.answer(
            f"🎉 *Викторина завершена!*\n"
            f"✅ Вы ответили правильно на *{score}* из *{total_questions}* вопросов.\n\nВыберите следующее действие из главного меню",
            parse_mode=ParseMode.MARKDOWN, reply_markup=get_main_menu_keyboard()
        )
        user_data.pop(user_id)

    await callback_query.answer()


async def send_question(message: Message, user_id: int):
    user_state = user_data[user_id]
    questions = user_state["questions"]
    current_question_index = user_state["current_question"]
    question: Question = questions[current_question_index]

    answers_text = "\n".join([f"{i + 1}. {answer}" for i, answer in enumerate(question.answers)])
    question_message = (
        f"❓ *Вопрос {current_question_index + 1}:*\n"
        f"{question.text}\n\n"
        f"*Варианты ответов:*\n"
        f"{answers_text}"
    )

    if user_state.get("message_id"):
        await message.bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=user_state["message_id"],
            text=question_message,
            reply_markup=get_answers_keyboard(
                question_index=current_question_index,
                answers=question.answers
            ),
            parse_mode=ParseMode.MARKDOWN
        )
    else:
        sent_message = await message.answer(
            question_message,
            reply_markup=get_answers_keyboard(
                question_index=current_question_index,
                answers=question.answers
            ),
            parse_mode=ParseMode.MARKDOWN
        )
        user_state["message_id"] = sent_message.message_id