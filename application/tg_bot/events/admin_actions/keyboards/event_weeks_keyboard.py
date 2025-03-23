import datetime
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from application.tg_bot.events.admin_actions.keyboards.callbacks import EventWeekCallback
from utils.get_week_start_end import get_week_start_end


def get_event_weeks_keyboard(month_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    start_date = datetime.datetime(year=datetime.datetime.now().year,month=month_id+1, day=1)
    current_date, _ = get_week_start_end(start_date)

    if  start_date.month != current_date.month:
        current_date = current_date + datetime.timedelta(days=7)

    while start_date.month == current_date.month:
        week_start, week_end = get_week_start_end(current_date)
        builder.button(text=f'{week_start.strftime("%d")}-{(week_end - datetime.timedelta(days=1)).strftime("%d")}', callback_data=EventWeekCallback(month_id=month_id+1,day_id=week_start.day))
        current_date = current_date + datetime.timedelta(days=7)

    builder.button(text="🔙 Назад", callback_data='view_events')
    builder.adjust(1)

    return builder.as_markup()

