from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from application.tg_bot.training.entities.theme import Theme


class ThemeCallback(CallbackData, prefix="theme"):
    theme_id: int

class ThemeListCallback(CallbackData, prefix="theme_list"):
    page: int

def get_theme_list_keyboard(theme_list: list[Theme], page: int, questions_per_page: int = 5) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    start_index = (page - 1) * questions_per_page
    end_index = min(start_index + questions_per_page, len(theme_list))

    for theme in theme_list[start_index:end_index]:
        builder.button(text=theme.name, callback_data=ThemeCallback(theme_id=theme.id))
    if page > 1:
        builder.button(text="⬅️ Назад", callback_data=ThemeListCallback(page=page - 1))
    if (page * questions_per_page) < len(theme_list):
       builder.button(text="Вперед ➡️", callback_data=ThemeListCallback(page=page + 1))

    builder.button(text="Создать тему", callback_data="theme_create_button")
    builder.button(text="🔙 В меню", callback_data="back_to_admin_main_menu")
    builder.button(text=f"Страница {page}", callback_data="ignore")

    builder.adjust(1)
    if page > 1 and (page * questions_per_page) < len(theme_list):
        builder.adjust( *[1 for i in range(5)],2,1,1,1)

    return builder.as_markup()