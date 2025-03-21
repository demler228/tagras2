from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from .callback_factories import QuizCallbackFactory


def get_themes_keyboard(themes, page: int = 1) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for theme in themes:
        print(theme)
        builder.button(
            text=theme.name,
            callback_data=QuizCallbackFactory(
                action="select_theme",
                theme_id=theme.id
            )
        )
    builder.adjust(1)
    return builder.as_markup()


def get_answers_keyboard(question_index: int, answers: list) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for i, answer in enumerate(answers):
        builder.button(
            text=f"🔹 {i+1} Ответ",
            callback_data=QuizCallbackFactory(
                action="answer",
                question_index=question_index,
                answer_index=i
            )
        )
    builder.adjust(1)
    return builder.as_markup()

def get_quiz_navigation_keyboard(question_index: int, total_questions: int, page: int = 1) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    if question_index > 0:
        builder.button(
            text="⬅️ Назад",
            callback_data=QuizCallbackFactory(
                action="prev",
                question_index=question_index - 1,
                page=page
            )
        )

    if question_index < total_questions - 1:
        builder.button(
            text="➡️ Вперед",
            callback_data=QuizCallbackFactory(
                action="next",
                question_index=question_index + 1,
                page=page
            )
        )

    builder.adjust(2)
    return builder.as_markup()