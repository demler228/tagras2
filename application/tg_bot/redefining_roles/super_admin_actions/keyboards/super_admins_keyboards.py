from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from .callback_factory import BackToUsersList, BackToAdminActions


def get_role_management_keyboard(user_id: int, user_role: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    if user_role == "user":
        builder.button(text="Назначить админом", callback_data=f"make_admin:{user_id}")
    elif user_role == "admin":
        builder.button(text="Убрать привилегию", callback_data=f"remove_admin:{user_id}")

    builder.button(text="Отмена", callback_data=BackToUsersList())
    builder.adjust(1)

    return builder.as_markup()
