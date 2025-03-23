from datetime import datetime

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from application.tg_bot.events.admin_actions.keyboards.callbacks import EventMonthCallback, EventWeekCallback
from utils.constants import months
from utils.get_week_start_end import get_week_start_end


def get_event_months_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    start_date, _ = get_week_start_end(datetime.now())
    builder.button(text="Текущая неделя", callback_data=EventWeekCallback(month_id=start_date.month, day_id=start_date.day))
    for i in range(12):
        builder.button(text=months[i], callback_data=EventMonthCallback(month_id=i))

    builder.button(text="🔙 Назад", callback_data='events_button_admin')
    builder.adjust(1,3,3,3,3,1)

    return builder.as_markup()

