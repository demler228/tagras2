from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from application.tg_bot.events.admin_actions.keyboards.callbacks import BackToEventMenuCallback, ChangeUserStateCallback
from application.tg_bot.events.entites.userMember import UserMember
from utils.logs import program_logger

def get_users_event_keyboard(text: str, members: list[UserMember], event_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for member in members:
        checked_icon = '✅ ' if member.is_member else ''
        username_with_checkmark = f'{checked_icon}{member.username}'  # Конкатенация иконки и имени пользователя
        builder.button(text=username_with_checkmark, callback_data=ChangeUserStateCallback(text=text, user_id=member.id, is_member=member.is_member))

    builder.button(text="🔙 Назад", callback_data=BackToEventMenuCallback(event_id=event_id))
    builder.adjust(1)

    return builder.as_markup()
