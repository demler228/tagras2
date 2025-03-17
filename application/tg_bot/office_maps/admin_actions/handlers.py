from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import FSInputFile, InputMediaPhoto, Message
from loguru import logger

from domain.office_maps.db_bl import MapsDbBl
from utils.config import settings
from .keyboards import (
    get_buildings_keyboard,
    get_floors_keyboard,
    get_sections_keyboard,
    get_section_keyboard)
from .keyboards import (
    BuildingCallbackFactory,
    FloorCallbackFactory,
    SectionCallbackFactory,
    BackToBuildingCallbackFactory,
)
from utils.data_state import DataSuccess
from .keyboards.callback_factories import DeleteBuildingCallbackFactory
from ..entities.building import Building

router = Router()

class AdminStates(StatesGroup):
    building_menu = State()
    floor_menu = State()
    section_menu = State()
    change_building_name = State()
    change_building_photo = State()
    create_building_name = State()
    create_building_photo = State()
    change_floor_name = State()
    change_floor_photo = State()
    create_floor_name = State()
    create_floor_photo = State()
    change_section_name = State()
    change_section_photo = State()
    create_section_name = State()
    create_section_photo = State()

@router.callback_query(FloorCallbackFactory.filter())
async def handle_floor_selection(
    callback_query: types.CallbackQuery,
    callback_data: FloorCallbackFactory
):
    floor_id = callback_data.floor_id
    building_id = callback_data.building_id

    # Получаем данные этажа
    data_state = MapsDbBl.get_floors_by_building(building_id)
    if isinstance(data_state, DataSuccess):
        floors = data_state.data
        floor = next((f for f in floors if f.id == floor_id), None)
        if floor:
            # Отправляем фото этажа с его именем
            media = InputMediaPhoto(
                media=FSInputFile(floor.photo_path),
                caption=f"Вы выбрали этаж: {floor.name}"
            )
            await callback_query.message.edit_media(
                media=media,
                reply_markup=get_sections_keyboard(building_id=building_id, floor_id=floor_id)
            )
        else:
            await callback_query.message.answer("Этаж не найден.")
    else:
        await callback_query.message.answer(data_state.message)

@router.callback_query(SectionCallbackFactory.filter())
async def handle_section_selection(
    callback_query: types.CallbackQuery,
    callback_data: SectionCallbackFactory
):
    section_id = callback_data.section_id
    floor_id = callback_data.floor_id
    building_id = callback_data.building_id

    # Получаем данные отдела
    data_state = MapsDbBl.get_sections_by_floor(floor_id)
    if isinstance(data_state, DataSuccess):
        sections = data_state.data
        section = next((s for s in sections if s.id == section_id), None)
        if section:
            # Отправляем фото отдела с его именем
            media = InputMediaPhoto(
                media=FSInputFile(section.photo_path),
                caption=f"Вы выбрали раздел: {section.name}"
            )
            await callback_query.message.edit_media(
                media=media,
                reply_markup=get_section_keyboard(building_id=building_id, floor_id=floor_id)
            )
        else:
            await callback_query.message.answer("Отдел не найден.")
    else:
        await callback_query.message.answer(data_state.message)

# Обработчик кнопки "Карта офиса"
@router.callback_query(F.data == "office_maps_button_admin")
@router.callback_query(BackToBuildingCallbackFactory.filter())
async def handle_office_maps_button(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.delete()

    answer = await callback_query.message.answer(
        "Выберите здание:",
        reply_markup=get_buildings_keyboard()
    )
    await state.update_data({'message': answer})

@router.callback_query(BuildingCallbackFactory.filter())
async def handle_floors_button(callback_query: types.CallbackQuery, callback_data: BuildingCallbackFactory, state: FSMContext):
        await floors_button(state,callback_query=callback_query,callback_data=callback_data)

async def floors_button(state: FSMContext, message: Message=None, building_id:int=None, callback_query: types.CallbackQuery=None, callback_data: BuildingCallbackFactory=None):
    await state.set_state(AdminStates.building_menu)
    if callback_query:
        building_id = callback_data.building_id
        message = callback_query.message
        await message.delete()
    else:
        await (await state.get_data())['message'].delete()

    data_state = MapsDbBl.get_buildings()  # Получаем список всех зданий
    if isinstance(data_state, DataSuccess):
        buildings = data_state.data
        # Ищем здание по ID
        building = next((b for b in buildings if b.id == building_id), None)
        if building:
            # Отправляем фото здания с его именем
            answer = await message.answer_photo(
                photo=FSInputFile(building.photo_path),
                caption=f"Вы выбрали здание: {building.name}",
                reply_markup=get_floors_keyboard(building_id=building_id)
            )
            await state.update_data({'message': answer}) #!!!!!!!!!
        else:
            await message.answer("Здание не найдено.")
    else:
        await message.answer(data_state.message)

@router.callback_query(F.data == "create_building")
async def building_create_name(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(AdminStates.create_building_name)
    await callback_query.message.answer(f"✍️ Введите название здания")

@router.message(F.text, AdminStates.create_building_name)
async def building_create_photo(message: Message, state: FSMContext):
    await state.update_data({'building_name': message.text})
    await state.set_state(AdminStates.create_building_photo)
    await message.answer(f"✍️ Отправьте фото")

@router.message(F.photo, AdminStates.create_building_photo)
async def building_create(message: Message, state: FSMContext):
    try:
        image_path = f'{settings.IMAGES_PATH}\\map\\buildings\\{message.photo[-1].file_id}.png'
        await message.bot.download(file=message.photo[-1].file_id,destination= image_path)
        building = Building(name=(await state.get_data())['building_name'],photo_path=image_path)
        data_state = MapsDbBl.create_building(building)
        if isinstance(data_state, DataSuccess):
            building_id = data_state.data
            await floors_button(state,message=message, building_id=building_id)
        else:
            await message.answer(f'❌ {data_state.error_message}')
    except Exception as ex:
        logger.exception(ex)
        await message.answer(f'❌ Ошибка отправки сообщения!')

@router.callback_query(DeleteBuildingCallbackFactory.filter())
async def delete_building_button(callback_query: types.CallbackQuery, callback_data: BuildingCallbackFactory, state: FSMContext):
    data_state = MapsDbBl.delete_building(callback_data.building_id)
    if isinstance(data_state, DataSuccess):
        await handle_office_maps_button(callback_query, state)
    else:
        await callback_query.message.answer(f'❌ {data_state.error_message}')