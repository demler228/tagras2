from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_exit_button_ai() -> ReplyKeyboardMarkup:
    exit_button = KeyboardButton(text="Вернуться в меню")

    reply_keyboard = ReplyKeyboardMarkup(
        keyboard=[[exit_button]],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    return reply_keyboard