from datetime import datetime

from aiogram.filters.callback_data import CallbackData

class ChangeMemberStateCallback(CallbackData, prefix="change_member_state"):
    user_id: int

class BackToEventMenuCallback(CallbackData, prefix="back_to_event_menu"):
    event_id: int

class ChangeUserStateCallback(CallbackData, prefix="change_member_state"):
    text: str
    user_id: int
    is_member: bool

class EventMonthCallback(CallbackData, prefix="event_month"):
    month_id: int

class EventWeekCallback(CallbackData, prefix="event_week"):
    month_id: int
    day_id: int

class EventMenuFromCalendarCallback(CallbackData, prefix="event_calendar"):
    month_id: int
    day_id: int
    event_id: int