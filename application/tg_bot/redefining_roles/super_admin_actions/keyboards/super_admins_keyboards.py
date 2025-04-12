from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from .callback_factory import BackToUsersList, BackToAdminActions, MakeRemoveAdminAction


def get_role_management_keyboard(user_id: int, user_role: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    if user_role == "user":
        builder.button(text="Назначить админом",
                       callback_data=MakeRemoveAdminAction(action="make_admin", user_id=user_id))

    elif user_role == "admin":
        builder.button(text="Убрать привилегию",
                       callback_data=MakeRemoveAdminAction(action="remove_admin", user_id=user_id))

    builder.button(text="🔙 Назад к списку", callback_data=BackToUsersList())
    builder.adjust(1)

    return builder.as_markup()


def back_to_admin_actions() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="🔙 Назад к действиям",
        callback_data=BackToAdminActions()
    )
    builder.adjust(1)
    return builder.as_markup()
