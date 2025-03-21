from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_user_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="Полезные контакты", callback_data="contacts_button")
    return builder.as_markup()