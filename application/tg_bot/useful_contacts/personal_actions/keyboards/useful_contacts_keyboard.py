from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_user_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="Ключевые сотрдуники", callback_data="key_users_button")
    builder.button(text="Список отделов", callback_data="useful_contacts_button")
    return builder.as_markup()