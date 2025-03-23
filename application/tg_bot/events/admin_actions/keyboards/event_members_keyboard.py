from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from application.tg_bot.events.admin_actions.keyboards.callbacks import ChangeMemberStateCallback, \
    BackToEventMenuCallback
from application.tg_bot.events.entites.userMember import UserMember

def get_members_event_keyboard( members: list[UserMember], event_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for member in members:
        builder.button(text=member.username, callback_data=ChangeMemberStateCallback(user_id=member.id))

    builder.button(text="🔙 Назад", callback_data=BackToEventMenuCallback(event_id=event_id))
    builder.adjust(1)

    return builder.as_markup()

