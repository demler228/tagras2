from datetime import datetime
import datetime as dd
from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from application.tg_bot.events.admin_actions.keyboards.callbacks import EventMonthCallback, EventWeekCallback, \
    EventMenuFromCalendarCallback
from application.tg_bot.events.admin_actions.keyboards.event_members_keyboard import ChangeMemberStateCallback, \
    get_members_event_keyboard
from application.tg_bot.events.admin_actions.keyboards.event_months_keyboard import get_event_months_keyboard
from application.tg_bot.events.admin_actions.keyboards.event_users_keyboard import get_users_event_keyboard, \
    ChangeUserStateCallback, BackToEventMenuCallback
from application.tg_bot.events.admin_actions.keyboards.event_menu_keyboard import get_event_menu_keyboard
from application.tg_bot.events.admin_actions.keyboards.event_start_keyboard import get_event_start_keyboard
from application.tg_bot.events.admin_actions.keyboards.event_weeks_keyboard import get_event_weeks_keyboard
from application.tg_bot.events.admin_actions.keyboards.events_for_week import get_events_for_week_keyboard
from application.tg_bot.events.entites.event import Event
from domain.events.db_bl import EventDbBl
from utils.constants import months
from utils.data_state import DataSuccess
from utils.logs import admin_logger

router = Router()

class AdminStates(StatesGroup):
    event_menu = State()
    create_event_name = State()
    create_event_description = State()
    create_event_date = State()
    change_event_name = State()
    change_event_description = State()
    change_event_data = State()
    add_member = State()
    users_choose = State()
    remove_member = State()

def get_date(str_date: str) -> datetime:
    try:
        lst = str_date.split()
        if len(lst) == 5:
            return datetime(year=int(lst[2]), month=int(lst[1]),day=int(lst[0]),hour=int(lst[3]),minute=int(lst[4]))
    except Exception:
        pass

@router.callback_query(F.data == "events_button_admin")
async def handle_events_button(callback_query: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback_query.message.delete()
    await callback_query.message.answer('Вы в разделе мероприятия.',reply_markup=get_event_start_keyboard())

@router.callback_query(F.data == "create_event")
async def handle_create_event_button(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.delete()
    await state.set_state(AdminStates.create_event_name)
    await callback_query.message.answer('✍️ Введите название мероприятия:')

@router.message(F.text, AdminStates.create_event_name)
async def handle_create_event_name(message: Message, state: FSMContext):
    await state.update_data({'event_name': message.text})
    await state.set_state(AdminStates.create_event_description)
    await message.answer('✍️ Введите описание мероприятия:')

@router.message(F.text,AdminStates.create_event_description)
async def handle_create_event_description(message: Message, state: FSMContext):
    await state.update_data({'event_description': message.text})
    await state.set_state(AdminStates.create_event_date)
    await message.answer('✍️ Введите дату мероприятия в формате dd mm yyyy HH MM(20 03 2025 16 56):')

@router.message(F.text,AdminStates.create_event_date)
async def handle_create_event_date(message: Message, state: FSMContext):
    date = get_date(message.text)
    if date:
        data_state = EventDbBl.create_event(Event(name=(await state.get_data())['event_name'],description=(await state.get_data())['event_description'],date=date))
        if isinstance(data_state, DataSuccess):
            admin_logger.info(
                f'Админ {message.chat.full_name} ({message.chat.id} создал новое мероприятие {(await state.get_data())['event_name']})')
            await event_menu_button(state, message, data_state.data)
        else:
            await message.answer(f'❌ {data_state.error_message}')
    else:
        await message.answer('❌ Неверно ввели дату!\nВведите дату мероприятия в формате dd mm yyyy HH MM(20 03 2025 16 56):')

@router.callback_query(EventMenuFromCalendarCallback.filter())
@router.callback_query(BackToEventMenuCallback.filter())
async def handle_event_menu_button(callback_query: types.CallbackQuery,
                                   callback_data: [BackToEventMenuCallback, EventMenuFromCalendarCallback],
                                   state: FSMContext):
        event_id = callback_data.event_id
        message = callback_query.message
        if isinstance(callback_data, EventMenuFromCalendarCallback):
            await state.update_data({'calendar': EventWeekCallback(month_id=callback_data.month_id,day_id=callback_data.day_id)})
        await message.delete()
        try:
            await (await state.get_data())['message'].delete()
        except Exception:
            pass
        await  event_menu_button(state,message=callback_query.message,event_id=event_id)


async def event_menu_button(state: FSMContext, message: Message, event_id: int):
    await state.set_state(AdminStates.event_menu)

    data_state = EventDbBl.get_event(event_id)
    if isinstance(data_state, DataSuccess):
        event = data_state.data
        data_state = EventDbBl.get_event_members(event_id)
        if isinstance(data_state, DataSuccess):
            callback = 'events_button_admin'
            if 'calendar' in (await state.get_data()):
                callback = (await state.get_data())['calendar']

            message = await message.answer(f'📅 <b>{event.name}</b>\nОписание: {event.description}\n'
                                                   f'Дата: {event.date.strftime("%d.%m.%Y %H:%M")}\n'
                                            f'Участники:\n{'Участников нету' if len(data_state.data) == 0 else
                                            '\n'.join([f'<a href="{user.tg_username}">{user.username}</a>'
                                                       for user in data_state.data])}\n\n❕ Чтобы добавить участника, напишите его имя.',
                                           parse_mode='HTML',
                                           reply_markup=get_event_menu_keyboard(event_id,callback))
            await state.update_data({'event': event,'message':message})
        else:
            await message.answer(f'❌ {data_state.error_message}')
    else:
        await message.answer(f'❌ {data_state.error_message}')

@router.callback_query(F.data == 'change_event_name')
async def change_event_name(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(AdminStates.change_event_name)
    await callback_query.message.answer(f"✍️ Введите новое название")


@router.message(F.text, AdminStates.change_event_name)
async def changed_event_name(message: Message, state: FSMContext):
    event = (await state.get_data())['event']
    old_event_name = event.name
    event.name = message.text
    data_state = EventDbBl.update_event(event)

    if isinstance(data_state, DataSuccess):
        admin_logger.info(
            f'Админ {message.chat.full_name} ({message.chat.id} изменил название мероприятия с {old_event_name} на {message.text})')
        await (await state.get_data())['message'].delete()
        await event_menu_button(state, message=message, event_id=event.id)
    else:
        await message.answer(f'❌ {data_state.error_message}')

@router.callback_query(F.data == 'change_event_description')
async def change_event_description(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(AdminStates.change_event_description)
    await callback_query.message.answer(f"✍️ Введите новое описание")

@router.message(F.text, AdminStates.change_event_description)
async def changed_event_description(message: Message, state: FSMContext):
    event = (await state.get_data())['event']
    old_event_description = event.description
    event.description = message.text
    data_state = EventDbBl.update_event(event)

    if isinstance(data_state, DataSuccess):
        admin_logger.info(
            f'Админ {message.chat.full_name} ({message.chat.id} изменил название мероприятия с {old_event_description} на {message.text})')
        await (await state.get_data())['message'].delete()
        await event_menu_button(state, message=message, event_id=event.id)
    else:
        await message.answer(f'❌ {data_state.error_message}')

@router.callback_query(F.data == 'change_event_date')
async def change_event_date(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(AdminStates.change_event_data)
    await callback_query.message.answer(f"✍️ Введите дату мероприятия в формате dd mm yyyy HH MM(20 03 2025 16 56):")

@router.message(F.text, AdminStates.change_event_data)
async def changed_event_date(message: Message, state: FSMContext):
    event = (await state.get_data())['event']
    old_date = event.date
    date = get_date(message.text)
    if date:
        event.date =date

        data_state = EventDbBl.update_event(event)
        if isinstance(data_state, DataSuccess):
            admin_logger.info(
                f'Админ {message.chat.full_name} ({message.chat.id} изменил дату мероприятия с {old_date} на {date})')
            await (await state.get_data())['message'].delete()
            await event_menu_button(state, message=message, event_id=event.id)
        else:
            await message.answer(f'❌ {data_state.error_message}')
    else:
        await message.answer('❌ Неверно ввели дату!\nВведите дату мероприятия в формате dd mm yyyy HH MM(20 03 2025 16 56):')

@router.callback_query(F.data == 'delete_event')
async def delete_event_button(callback_query: types.CallbackQuery, state: FSMContext):
    event = (await state.get_data())['event']
    data_state = EventDbBl.delete_event(event)
    if isinstance(data_state, DataSuccess):
        admin_logger.info(
            f'Админ {callback_query.message.chat.full_name} ({callback_query.message.chat.id} удалил мероприятие {event.name})')
        if 'calendar' in (await state.get_data()):
            await choose_week_event(callback_query, state, (await state.get_data())['calendar'])
        else:
            await handle_events_button(callback_query, state)
    else:
        await callback_query.message.answer(f'❌ {data_state.error_message}')

@router.message(F.text, AdminStates.users_choose)
@router.message(F.text, AdminStates.event_menu)
async def choose_users_event(message: Message, state: FSMContext):
    if await state.get_state() == AdminStates.users_choose:
        await (await state.get_data())['choose_message'].delete()
    event = (await state.get_data())['event']
    await state.set_state(AdminStates.users_choose)
    data_state = EventDbBl.get_users_by_name(message.text, event.id)
    if isinstance(data_state, DataSuccess):
        choose_message = await  message.answer(f'{f'Найдено {len(data_state.data)} {'пользователей'if len(data_state.data) > 4 else
        'пользователя' if len(data_state.data) > 1 else 'пользователь'}:'if len(data_state.data) > 0
        else '❌ Пользователей с таким именем не найдено!'}', reply_markup=get_users_event_keyboard(message.text,data_state.data, event.id))

        await state.update_data({'choose_message':choose_message})
    else:
        await message.answer(f'❌ {data_state.error_message}')

@router.callback_query(ChangeUserStateCallback.filter())
async def update_choose_members_event(callback_query: types.CallbackQuery, state: FSMContext, callback_data: ChangeUserStateCallback):
    event = (await state.get_data())['event']
    message = (await state.get_data())['message']
    data_state  = EventDbBl.change_member_state(callback_data.user_id,callback_data.is_member,event) # добавляем или удаляем юзера из мероприятия
    if isinstance(data_state, DataSuccess):
        admin_logger.info(
            f'Админ {callback_query.message.chat.full_name} ({callback_query.message.chat.id} изменил список участников мероприятия {event.name})')
        data_state = EventDbBl.get_users_by_name(callback_data.text, event.id) # получем обновленный список пользователей с их принадлежностью к мероприятию
        if isinstance(data_state, DataSuccess):
            await callback_query.message.edit_reply_markup(reply_markup=get_users_event_keyboard(callback_data.text, data_state.data,event.id))
            data_state = EventDbBl.get_event(event.id) # получаем актуальные данные о мероприятии
            if isinstance(data_state, DataSuccess):
                event = data_state.data
                data_state = EventDbBl.get_event_members(event.id) # обновляем наше сообщение о мероприятии
                if isinstance(data_state, DataSuccess):
                    await message.edit_text(f'📅 <b>{event.name}</b>\nОписание: {event.description}\n'
                                                   f'Дата: {event.date.strftime("%d.%m.%Y %H:%M")}\n'
                                            f'Участники:\n {'Участников нету' if len(data_state.data) == 0 else
                                            '\n'.join([f'<a href="{user.tg_username}">{user.username}</a>'
                                                       for user in data_state.data])}',parse_mode='HTML')
                    return

        await callback_query.message.answer(f'❌ {data_state.error_message}')

@router.callback_query(F.data == 'change_event_members')
async def members_event(callback_query: types.CallbackQuery,state: FSMContext):
    await callback_query.message.delete()

    await  state.set_state(AdminStates.remove_member)
    event = (await state.get_data())['event']
    await state.set_state(AdminStates.users_choose)
    data_state = EventDbBl.get_event_members(event.id)
    if isinstance(data_state, DataSuccess):
        await callback_query.message.answer('Нажмите на пользователя, которого хотите удалить:', reply_markup=get_members_event_keyboard(data_state.data, event.id))
    else:
        await callback_query.message.answer(f'❌ {data_state.error_message}')

@router.callback_query(ChangeMemberStateCallback.filter())
async def update_choose_members_event(callback_query: types.CallbackQuery, state: FSMContext, callback_data: ChangeUserStateCallback):
    event = (await state.get_data())['event']
    data_state  = EventDbBl.change_member_state(callback_data.user_id,True,event)
    if isinstance(data_state, DataSuccess):
        admin_logger.info(
            f'Админ {callback_query.message.chat.full_name} ({callback_query.message.chat.id} изменил список участников мероприятия {event.name})')
        data_state = EventDbBl.get_event_members(event.id)
        if isinstance(data_state, DataSuccess):
            await members_event(callback_query,state)
            return
    await callback_query.message.answer(f'❌ {data_state.error_message}')

@router.callback_query(F.data == 'view_events')
async def choose_month_event(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.delete()
    await  callback_query.message.answer('Выберите месяц:',reply_markup=get_event_months_keyboard())

@router.callback_query(EventMonthCallback.filter())
async def choose_week_event(callback_query: types.CallbackQuery, state: FSMContext, callback_data: EventMonthCallback):
    await callback_query.message.delete()
    await  callback_query.message.answer(f'Выбран: <b>{months[callback_data.month_id]}</b>\nВыберите неделю:', reply_markup=get_event_weeks_keyboard(callback_data.month_id),parse_mode='HTML')

@router.callback_query(EventWeekCallback.filter())
async def choose_week_event(callback_query: types.CallbackQuery, state: FSMContext, callback_data: EventWeekCallback):
    await callback_query.message.delete()
    start_date = datetime(year=datetime.now().year, month=callback_data.month_id, day=callback_data.day_id)
    end_date = start_date + dd.timedelta(days=6)
    data_state = EventDbBl.get_all_events_for_week(start_date, end_date)
    if isinstance(data_state, DataSuccess):
        events = data_state.data
        await  callback_query.message.answer(f'🗓️ Мероприятия за <b>{start_date.strftime("%d.%m.%Y")}</b> по'
                                             f' <b>{end_date.strftime("%d.%m.%Y")}</b>\nВыберите мероприятие:',
                                             reply_markup=get_events_for_week_keyboard(events,start_date),parse_mode='HTML')
    else:
        await callback_query.message.answer(f'❌ {data_state.error_message}')