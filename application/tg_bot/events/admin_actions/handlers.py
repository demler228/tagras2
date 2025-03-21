from datetime import datetime
from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from application.tg_bot.events.admin_actions.keyboards.event_menu_keyboard import get_event_menu_keyboard
from application.tg_bot.events.admin_actions.keyboards.event_start_keyboard import get_event_start_keyboard
from application.tg_bot.events.entites.event import Event
from domain.events.db_bl import EventDbBl
from utils.data_state import DataSuccess

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
            await event_menu_button(state, message, data_state.data)
        else:
            await message.answer(f'❌ {data_state.error_message}')
    else:
        await message.answer('❌ Неверно ввели дату!\nВведите дату мероприятия в формате dd mm yyyy HH MM(20 03 2025 16 56):')

# @router.callback_query(AdminBuildingCallbackFactory.filter())
# async def handle_event_menu_button(callback_query: types.CallbackQuery, callback_data: AdminBuildingCallbackFactory, state: FSMContext):
#         await floors_button(state,callback_query=callback_query,callback_data=callback_data)

async def event_menu_button(state: FSMContext, message: Message=None, event_id:int=None, callback_query: types.CallbackQuery=None):
    await state.set_state(AdminStates.event_menu)
    # if callback_query:
    #     pass # пока нету просмотра всех событий
    #     # event_id = callback_data.event_id
    #     # message = callback_query.message
    #     # await message.delete()
    # else:


    data_state = EventDbBl.get_event(event_id)
    if isinstance(data_state, DataSuccess):
        event = data_state.data
        message = await message.answer(f'Название: {event.name}\nОписание: {event.description}\nДата: {event.date.strftime("%d.%m.%Y %H:%M")}', reply_markup=get_event_menu_keyboard())
        await state.update_data({'event': event,'message':message})
    else:
        await message.answer(f'❌ {data_state.error_message}')

@router.callback_query(F.data == 'change_event_name')
async def change_event_name(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(AdminStates.change_event_name)
    await callback_query.message.answer(f"✍️ Введите новое название")


@router.message(F.text, AdminStates.change_event_name)
async def changed_event_name(message: Message, state: FSMContext):
    event = (await state.get_data())['event']
    event.name = message.text
    data_state = EventDbBl.update_event(event)

    if isinstance(data_state, DataSuccess):
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
    event.description = message.text
    data_state = EventDbBl.update_event(event)

    if isinstance(data_state, DataSuccess):
        await (await state.get_data())['message'].delete()
        await event_menu_button(state, message=message, event_id=event.id)
    else:
        await message.answer(f'❌ {data_state.error_message}')

@router.callback_query(F.data == 'change_event_date')
async def change_event_date(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(AdminStates.create_event_date)
    await callback_query.message.answer(f"✍️ Введите дату мероприятия в формате dd mm yyyy HH MM(20 03 2025 16 56):")

@router.message(F.text, AdminStates.create_event_date)
async def changed_event_date(message: Message, state: FSMContext):
    event = (await state.get_data())['event']
    date = get_date(message.text)
    if date:
        event.date =date

        data_state = EventDbBl.update_event(event)
        if isinstance(data_state, DataSuccess):
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
        await (await state.get_data())['message'].delete()
        await handle_events_button(callback_query,state)
        await callback_query.message.answer(f'❌ {data_state.error_message}')