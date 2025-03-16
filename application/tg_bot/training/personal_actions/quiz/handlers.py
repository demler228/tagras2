from aiogram import Router, types, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.enums import ParseMode
from domain.quiz.db_bl import DBService
from domain.quiz.db_dal import DBRepository
from .keyboards import get_answers_keyboard, get_themes_keyboard
from .callback_factories import QuizCallbackFactory

router = Router()

user_data = {}

@router.callback_query(F.data == "quiz_button")
async def handle_quiz_button(callback_query: types.CallbackQuery):
    themes = DBService.get_themes()
    if not themes:
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

    questions = DBService.get_questions_by_theme(theme_id)
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

    selected_answer = callback_data.answer
    questions = user_state["questions"]
    current_question_index = user_state["current_question"]
    current_question = questions[current_question_index]

    correct_answer = current_question["correct_answer"]
    if selected_answer == correct_answer:
        user_state["score"] += 1

    user_state["current_question"] += 1
    if user_state["current_question"] < len(questions):
        await send_question(callback_query.message, user_id)
    else:
        # Викторина завершена
        score = user_state["score"]
        total_questions = len(questions)
        
        # Удаляем сообщение с вопросами
        await callback_query.message.bot.delete_message(
            chat_id=callback_query.message.chat.id,
            message_id=user_state["message_id"]
        )

        # Отправляем сообщение с результатами
        await callback_query.message.answer(
            f"🎉 *Викторина завершена!*\n"
            f"✅ Вы ответили правильно на *{score}* из *{total_questions}* вопросов.",
            parse_mode=ParseMode.MARKDOWN
        )
        user_data.pop(user_id)

    await callback_query.answer()

async def send_question(message: Message, user_id: int):
    user_state = user_data[user_id]
    questions = user_state["questions"]
    current_question_index = user_state["current_question"]
    question_data = questions[current_question_index]

    question_text = question_data["question_text"]
    answers = question_data["answers"]

    answers_text = "\n".join([f"{i + 1}. {answer}" for i, answer in enumerate(answers)])
    question_message = (
        f"❓ *Вопрос {current_question_index + 1}:*\n"
        f"{question_text}\n\n"
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
                answers=answers
            ),
            parse_mode=ParseMode.MARKDOWN
        )
    else:
        sent_message = await message.answer(
            question_message,
            reply_markup=get_answers_keyboard(
                question_index=current_question_index,
                answers=answers
            ),
            parse_mode=ParseMode.MARKDOWN
        )
        user_state["message_id"] = sent_message.message_id