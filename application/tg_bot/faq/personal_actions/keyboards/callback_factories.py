from aiogram.filters.callback_data import CallbackData

class FaqCallbackFactory(CallbackData, prefix="faq"):
    action: str
    page: int
    question_index: int

class BackToMenuCallbackFactory(CallbackData, prefix="back_to_menu"):
    pass