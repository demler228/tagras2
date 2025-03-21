import datetime
from aiogram import Router, F, types
from application.tg_bot.events.personal_actions.keyboards.events_keyboard import EventsCallbackFactory, \
    get_events_keyboard
from domain.events.db_bl import EventDbBl
from utils.data_state import DataSuccess
from utils.get_week_start_end import get_week_start_end

router = Router()

week_days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']

@router.callback_query(F.data == "events_button")
@router.callback_query(EventsCallbackFactory.filter())
async def handle_events_button(callback_query: types.CallbackQuery, callback_data:EventsCallbackFactory=None):
    await callback_query.message.delete()

    telegram_id = callback_query.from_user.id
    offset = 0
    if callback_data:
        offset = callback_data.offset
    start_date, end_date = get_week_start_end(datetime.date.today(), offset)

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
            text = f'🗓️ Мероприятия за {start_date.strftime("%d.%m.%Y")} по {(end_date - datetime.timedelta(days=1)).strftime("%d.%m.%Y")}'
        # заполняем дни недели мероприятиями
        for i,day in enumerate(week_days):
            current_date = start_date + datetime.timedelta(days=i)
            text += f'\n{day} {current_date.strftime("%d.%m.%Y")}:'
            this_day_events = [] # этот список нужен только чтобы проверить потом, есть ли задачи на этот день
            for event in events:
                if event.date.day == current_date.day:
                    this_day_events.append(event)
                    text += f'\n\t\t<b>{event.name}</b> - {event.description}'
            if len(this_day_events) == 0:
                text+='\n\t\tНету мероприятий.'
            text += '\n'

        await callback_query.message.answer(
            text,
            parse_mode='HTML',
            reply_markup=get_events_keyboard(offset=offset)
        )
    else:
        await callback_query.message.answer(
           f'❌ {data_state.error_message}')

