import datetime
from datetime import  timedelta
from typing import Tuple, Any


def get_week_start_end(date: datetime,offset:int) -> tuple[timedelta | Any, timedelta | Any]:

    # Определяем день недели (0 — понедельник, 6 — воскресенье)
    weekday = date.weekday()

    # Вычисляем смещение до начала недели (понедельник)
    start_delta = datetime.timedelta(days=weekday)
    end_delta = datetime.timedelta(days=(7 - weekday))

    # Определяем начало и конец недели
    week_start = date - start_delta + datetime.timedelta(days=offset*7)
    week_end = date + end_delta + datetime.timedelta(days=offset*7)

    return week_start, week_end