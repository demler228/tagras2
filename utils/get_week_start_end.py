from datetime import datetime, timedelta
from typing import Tuple, Any
from xmlrpc.client import DateTime


def get_week_start_end(date_str) -> tuple[timedelta | datetime | Any, datetime | Any]:
    # Парсим строку даты в объект datetime
    date = datetime.strptime(date_str, "%d.%m.%Y")

    # Определяем день недели (0 — понедельник, 6 — воскресенье)
    weekday = date.weekday()

    # Вычисляем смещение до начала недели (понедельник)
    start_delta = datetime.timedelta(days=weekday)
    end_delta = datetime.timedelta(days=(7 - weekday))

    # Определяем начало и конец недели
    week_start = date - start_delta
    week_end = date + end_delta

    return week_start, week_end