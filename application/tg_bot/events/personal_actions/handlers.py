import datetime
from aiogram import Router, F, types
from application.tg_bot.events.personal_actions.keyboards.events_keyboard import EventsCallbackFactory, \
    get_events_keyboard
from domain.events.db_bl import EventDbBl
from utils.data_state import DataSuccess
from utils.get_week_start_end import get_week_start_end

router = Router()

week_days = ['Понедельник, Вторник, Среда, Четверг, Пятница, Суббота, Воскресенье']

@router.callback_query(F.data == "events_button")
@router.callback_query(EventsCallbackFactory.filter())
async def handle_events_button(callback_query: types.CallbackQuery, callback_data:EventsCallbackFactory=None):
    await callback_query.message.delete()

    start_date, end_date = get_week_start_end(datetime.datetime.now())
    telegram_id = callback_query.message.from_user.id
    offset = None
    if callback_data:
        offset = callback_data.offset

    data_state = EventDbBl.get_events_by_telegram_id(telegram_id, start_date, end_date)
    if isinstance(data_state, DataSuccess):
        events = data_state.data
        if offset == 0:
            text = "🗓️ Мероприятия на эту неделю:"
        elif offset == -1:
            text = "🗓️ Мероприятия за прошлую неделю"
        elif offset == 1:
            text = "🗓️ Мероприятия на следующую неделю"
        else:
            text = f'🗓️ Мероприятия за {events[0].date.strftime("%d.%m.%Y")} по {events[-1].date.strftime("%d.%m.%Y")}'
        # заполняем дни недели мероприятиями
        for i,day in enumerate(week_days):
            current_date = start_date + datetime.timedelta(days=i)
            text += f'\n{day} {current_date.strftime("%d.%m.%Y")}:'
            this_day_events = [] # этот список нужен только чтобы проверить потом, есть ли задачи на этот день
            for event in events:
                if event.date == current_date:
                    this_day_events += event
                    text += f'\n    {event.name} - {event.description}'
            if len(this_day_events) == 0:
                text+='\n    Нету мероприятий.'

        await callback_query.message.answer(
            text,
            reply_markup=get_events_keyboard(offset=offset)
        )
