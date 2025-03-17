from aiogram.filters.callback_data import CallbackData


class QuizCallbackFactory(CallbackData, prefix="quiz"):
    action: str
    theme_id: int | None = None
    question_index: int | None = None
    answer_index: int | None = None
    page: int = 1