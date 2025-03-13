from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder


class ThemeCallback(CallbackData, prefix="theme"):
    theme_id: int


def get_themes_keyboard(themes: list[tuple[int, str]]):
    builder = InlineKeyboardBuilder()

    for theme_id, theme_name in themes:
        builder.button(
            text=theme_name,
            callback_data=ThemeCallback(theme_id=theme_id)
        )

    builder.adjust(1)

    return builder.as_markup()
