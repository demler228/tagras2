from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


class EventsCallbackFactory(CallbackData, prefix="events"):
    offset: int

def get_events_keyboard(offset: int = 0) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="<---", callback_data=EventsCallbackFactory(offset=offset-1))
    builder.button(text="--->", callback_data=EventsCallbackFactory(offset=offset+1))
    builder.button(text="🔙 В меню", callback_data="back_to_main_menu")

    builder.adjust(2,1)

    return builder.as_markup()