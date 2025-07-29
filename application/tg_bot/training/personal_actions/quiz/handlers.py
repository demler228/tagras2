from aiogram import Router, types, F
from aiogram.types import Message, CallbackQuery
from aiogram.enums import ParseMode
from domain.quiz.db_bl import DBService
import random
from application.tg_bot.training.entities.questions import Question
from .keyboards import get_answers_keyboard, get_themes_keyboard
from .callback_factories import QuizCallbackFactory
from utils.data_state import DataSuccess
from application.tg_bot.menu.personal_actions.keyboards.menu_keyboard import get_main_menu_keyboard
from domain.quiz.db_dal import QuizRepository

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
        all_questions = questions_result.data
        questions = random.sample(all_questions, min(10, len(all_questions)))
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
    questions = user_state["questions"]
    current_question_index = user_state["current_question"]
    current_question: Question = questions[current_question_index]

    shuffled_answers = user_state["shuffled_answers"][current_question_index]
    selected_answer = shuffled_answers[selected_answer_index]
    correct_answer = current_question.correct_answer

    if selected_answer == correct_answer:
        user_state["score"] += 1
        await callback_query.answer("✅ Верно!")
    else:
        await callback_query.answer("❌ Неверно!")

    user_state["current_question"] += 1
    if user_state["current_question"] < len(questions):
        await send_question(callback_query.message, user_id)
    else:
        score = user_state["score"]
        theme_id = questions[0].theme_id

        save_result = QuizRepository.save_quiz_result(
            user_id=user_id,
            theme_id=theme_id,
            score=score
        )

        if user_state.get("message_id"):
            try:
                await callback_query.message.bot.delete_message(
                    chat_id=callback_query.message.chat.id,
                    message_id=user_state["message_id"]
                )
            except:
                pass

        is_admin = False

        if isinstance(save_result, DataSuccess):
            result_message = (
                f"🎉 *Викторина завершена!*\n"
                f"✅ Ваш счет: *{score}* правильных ответов\n"
                f"📊 Результат сохранен!\n\n"
                f"Выберите следующее действие из главного меню"
            )
        else:
            result_message = (
                f"🎉 *Викторина завершена!*\n"
                f"✅ Ваш счет: *{score}* правильных ответов\n"
                f"⚠️ Не удалось сохранить результат\n\n"
                f"Выберите следующее действие из главного меню"
            )

        await callback_query.message.answer(
            result_message,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=get_main_menu_keyboard(is_admin=is_admin)
        )
        user_data.pop(user_id)


async def send_question(message: Message, user_id: int):
    user_state = user_data[user_id]
    questions = user_state["questions"]
    current_question_index = user_state["current_question"]
    question: Question = questions[current_question_index]

    shuffled_answers = question.answers.copy()
    random.shuffle(shuffled_answers)

    if "shuffled_answers" not in user_state:
        user_state["shuffled_answers"] = [None] * len(questions)
    user_state["shuffled_answers"][current_question_index] = shuffled_answers

    answers_text = "\n".join([f"{i + 1}. {answer}" for i, answer in enumerate(shuffled_answers)])
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
                answers=shuffled_answers
            ),
            parse_mode=ParseMode.MARKDOWN
        )
    else:
        sent_message = await message.answer(
            question_message,
            reply_markup=get_answers_keyboard(
                question_index=current_question_index,
                answers=shuffled_answers
            ),
            parse_mode=ParseMode.MARKDOWN
        )
        user_state["message_id"] = sent_message.message_id