from datetime import datetime
from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from application.tg_bot.events.admin_actions.keyboards.event_keyboard import get_event_start_keyboard

router = Router()

class AdminStates(StatesGroup):
    event_menu = State()
    create_event_name = State()
    create_event_description = State()
    create_event_data = State()
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
async def handle_events_button(callback_query: types.CallbackQuery):
    await callback_query.message.answer('Вы в разделе мероприятия.',reply_markup=get_event_start_keyboard())

@router.callback_query(F.data == "create_event")
async def handle_create_event_button(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(AdminStates.create_event_name)
    await callback_query.message.answer('✍️ Введите название мероприятия:')

@router.callback_query(F.text,AdminStates.create_event_name)
async def handle_create_event_button(callback_query: types.CallbackQuery, state: FSMContext):
    await state.update_data({'event_name': callback_query.data})
    await state.set_state(AdminStates.create_event_description)
    await callback_query.message.answer('✍️ Введите описание мероприятия:')

@router.callback_query(F.text,AdminStates.create_event_description)
async def handle_create_event_button(callback_query: types.CallbackQuery, state: FSMContext):
    await state.update_data({'event_description': callback_query.data})
    await state.set_state(AdminStates.create_event_data)
    await callback_query.message.answer('✍️ Введите дату мероприятия в формате dd mm yyyy HH MM(20 03 2025 16 56):')

@router.callback_query(F.text,AdminStates.create_event_data)
async def handle_create_event_button(callback_query: types.CallbackQuery, state: FSMContext):
    date = get_date(callback_query.data)
    if date:

        await callback_query.message.answer('✍️ Введите дату мероприятия в формате dd mm yyyy HH MM(20 03 2025 16 56):')
    else:
        await callback_query.message.answer('❌ Неверно ввели дату!\nВведите дату мероприятия в формате dd mm yyyy HH MM(20 03 2025 16 56):')

# @router.callback_query(AdminBuildingCallbackFactory.filter())
# async def handle_event_menu_button(callback_query: types.CallbackQuery, callback_data: AdminBuildingCallbackFactory, state: FSMContext):
#         await floors_button(state,callback_query=callback_query,callback_data=callback_data)

# async def event_menu_button(state: FSMContext, message: Message=None, event_id:int=None, callback_query: types.CallbackQuery=None):
#     await state.set_state(AdminStates.event_menu)
#     if callback_query:
#         #building_id = callback_data.building_id
#         message = callback_query.message
#         await message.delete()
#     else:
#         await (await state.get_data())['message'].delete()
#
#     data_state = MapsDbBl.get_buildings()  # Получаем список всех зданий
#     if isinstance(data_state, DataSuccess):