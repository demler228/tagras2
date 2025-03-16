from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData


class ThemeCallback(CallbackData, prefix="theme"):
    action: str
    theme_id: int | None = None


def get_themes_keyboard(themes) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for theme in themes:
        builder.button(
            text=theme.name,
            callback_data=ThemeCallback(action="select", theme_id=theme.id).pack()
        )

    builder.button(text="🔙 В меню", callback_data="back_to_menu")
    builder.adjust(1)
    return builder.as_markup()


def get_materials_keyboard(theme_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="🔙 Назад к темам",
        callback_data=ThemeCallback(action="back").pack()
    )
    builder.button(text="🔙 В меню", callback_data="back_to_menu")
    builder.adjust(1)
    return builder.as_markup()
