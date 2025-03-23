from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_user_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="Ключевые сотрдуники", callback_data="key_users_button")
    builder.button(text="Список отделов", callback_data="department_list_button")
    builder.button(text="Назад в меню", callback_data="back_to_main_menu")
    builder.adjust(1)
    return builder.as_markup()