import datetime
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from application.tg_bot.events.admin_actions.keyboards.callbacks import EventMenuFromCalendarCallback, \
    EventMonthCallback, EventWeekCallback
from application.tg_bot.events.entites.event import Event
from utils.constants import week_days


def get_events_for_week_keyboard(events: list[Event],start_date: datetime) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    events_buttons = 0

    for i, day in enumerate(week_days):
        current_date = start_date + datetime.timedelta(days=i)
        this_day_events = []  # этот список нужен только чтобы проверить потом, есть ли задачи на этот день

        for event in events:
            if event.date.day == current_date.day:
                this_day_events.append(event)

        this_day_events = sorted(this_day_events,key=lambda event: event.date)
        if len(this_day_events) != 0:
            events_buttons += 1
            builder.button(text=f'⬇️{week_days[i]}⬇️',callback_data='None')
            for event in this_day_events:
                events_buttons += 1
                builder.button(text=f'{event.date.strftime("%H:%M")} {event.name}',
                                                          callback_data=EventMenuFromCalendarCallback(event_id=event.id,
                                                                                                      day_id=start_date.day
                                                                                                      ,month_id=start_date.month))
    date_plus = start_date + datetime.timedelta(days=7)
    date_minus = start_date - datetime.timedelta(days=7)
    builder.button(text="<---", callback_data=EventWeekCallback(month_id=date_minus.month, day_id=date_minus.day))
    builder.button(text="--->", callback_data=EventWeekCallback(month_id=date_plus.month, day_id=date_plus.day))
    builder.button(text="🔙 Назад", callback_data=EventMonthCallback(month_id=start_date.month-1))
    builder.adjust(*[1 for i in range(events_buttons)],2,1)

    return builder.as_markup()

