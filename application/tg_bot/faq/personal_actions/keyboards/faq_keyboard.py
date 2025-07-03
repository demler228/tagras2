from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from .callback_factories import FaqCallbackFactory

def get_faq_keyboard(page: int, total_questions: int, questions: list, questions_per_page: int = 5):
    """
    Creates an inline keyboard for FAQ navigation.
    """
    builder = InlineKeyboardBuilder()
    start_index = (page - 1) * questions_per_page
    end_index = min(start_index + questions_per_page, len(questions))

    for i in range(start_index, end_index):
        builder.button(
            text=questions[i].question,
            callback_data=FaqCallbackFactory(action="show", page=page, question_index=i)
        )

    if page > 1:
        builder.button(text="⬅️ Назад", callback_data=FaqCallbackFactory(action="prev", page=page - 1, question_index=0))
    if (page * questions_per_page) < total_questions:
        builder.button(text="Вперед ➡️", callback_data=FaqCallbackFactory(action="next", page=page + 1, question_index=0))

    builder.button(text="🔙 В меню", callback_data=BackToMenuCallbackFactory())
    builder.button(text=f"Страница {page}", callback_data="ignore")
    builder.adjust(1)
    return builder.as_markup()


def get_faq_answer_keyboard(page: int, question_index: int):
    """
    Creates an inline keyboard for returning to the question list.
    """
    builder = InlineKeyboardBuilder()
    builder.button(
        text="🔙 К списку вопросов",
        callback_data=FaqCallbackFactory(action="back", page=page, question_index=question_index)
    )
    builder.button(text="🔙 В меню", callback_data=BackToMenuCallbackFactory())
    return builder.as_markup()