import os

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
    AdminBuildingCallbackFactory,
    AdminFloorCallbackFactory,
    AdminSectionCallbackFactory,
)
from utils.data_state import DataSuccess
from ..entities.building import Building
from ..entities.floor import Floor
from ..entities.section import Section

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

@router.callback_query(AdminSectionCallbackFactory.filter())
async def handle_section_selection(callback_query: types.CallbackQuery, callback_data: AdminSectionCallbackFactory, state: FSMContext):
        await section_selection(state,callback_query=callback_query,callback_data=callback_data)


async def section_selection(
    state: FSMContext, message: Message=None, building_id:int=None,floor_id:int=None,section_id:int=None, callback_query: types.CallbackQuery=None,
    callback_data: AdminSectionCallbackFactory=None
):
    await state.set_state(AdminStates.building_menu)
    if callback_query:
        section_id = callback_data.section_id
        floor_id = callback_data.floor_id
        building_id = callback_data.building_id
        message = callback_query.message
        await message.delete()
    else:
        await (await state.get_data())['message'].delete()

    # Получаем данные отдела
    data_state = MapsDbBl.get_sections_by_floor(floor_id)
    if isinstance(data_state, DataSuccess):
        sections = data_state.data
        section = next((s for s in sections if s.id == section_id), None)

        photo = FSInputFile(f'{settings.IMAGES_PATH}\\assets\\image_not_found.jpg')
        if os.path.exists(section.photo_path):
            photo = FSInputFile(section.photo_path)

        answer = await message.answer_photo(
            photo=photo,
            caption=f"Вы выбрали отдел: {section.name}",
            reply_markup=get_section_keyboard(building_id=building_id, floor_id=floor_id)
        )
        await state.update_data({'message': answer,'section':section}) #!!!!!!!!!

    else:
        await callback_query.message.answer(data_state.message)

# Обработчик кнопки "Карта офиса"
@router.callback_query(F.data == "office_maps_button_admin")
async def handle_office_maps_button(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.delete()

    answer = await callback_query.message.answer(
        "Выберите здание:",
        reply_markup=get_buildings_keyboard()
    )
    await state.update_data({'message': answer})

@router.callback_query(AdminBuildingCallbackFactory.filter())
async def handle_floors_button(callback_query: types.CallbackQuery, callback_data: AdminBuildingCallbackFactory, state: FSMContext):
        await floors_button(state,callback_query=callback_query,callback_data=callback_data)

async def floors_button(state: FSMContext, message: Message=None, building_id:int=None, callback_query: types.CallbackQuery=None, callback_data: AdminBuildingCallbackFactory=None):
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

        photo = FSInputFile(f'{settings.IMAGES_PATH}\\assets\\image_not_found.jpg')
        if os.path.exists(building.photo_path):
            photo = FSInputFile(building.photo_path)

        answer = await message.answer_photo(
            photo=photo,
            caption=f"Вы выбрали здание: {building.name}",
            reply_markup=get_floors_keyboard(building_id=building_id)
        )
        await state.update_data({'message': answer,'building':building}) #!!!!!!!!!
    else:
        await message.answer(data_state.message)

@router.callback_query(AdminFloorCallbackFactory.filter())
async def handle_floors_selection(callback_query: types.CallbackQuery, callback_data: AdminFloorCallbackFactory, state: FSMContext):
        await floor_selection(state,callback_query=callback_query,callback_data=callback_data)


async def floor_selection(state: FSMContext, message: Message=None, building_id:int=None, floor_id:int=None, callback_query: types.CallbackQuery=None,
    callback_data: AdminFloorCallbackFactory=None
):
    await state.set_state(AdminStates.floor_menu)
    if callback_query:
        building_id = callback_data.building_id
        floor_id = callback_data.floor_id
        message = callback_query.message
        await message.delete()
    else:
        await (await state.get_data())['message'].delete()

    # Получаем данные этажа
    data_state = MapsDbBl.get_floors_by_building(building_id)
    if isinstance(data_state, DataSuccess):
        floors = data_state.data
        floor = next((f for f in floors if f.id == floor_id), None)

        photo = FSInputFile(f'{settings.IMAGES_PATH}\\assets\\image_not_found.jpg')
        if os.path.exists(floor.photo_path):
            photo = FSInputFile(floor.photo_path)

        answer = await message.answer_photo(
            photo=photo,
            caption=f"Вы выбрали этаж: {floor.name}",
            reply_markup=get_sections_keyboard(building_id=building_id, floor_id=floor_id)
        )
        await state.update_data({'message': answer,'floor':floor}) #!!!!!!!!!

    else:
        await callback_query.message.answer(data_state.message)

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

@router.callback_query(F.data == 'delete_building')
async def delete_building_button(callback_query: types.CallbackQuery, state: FSMContext):
    building = (await state.get_data())['building']
    data_state = MapsDbBl.delete_building(building)
    if isinstance(data_state, DataSuccess):
        await handle_office_maps_button(callback_query, state)
    else:
        await callback_query.message.answer(f'❌ {data_state.error_message}')

@router.callback_query(F.data == "create_floor")
async def floor_create_name(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(AdminStates.create_floor_name)
    await callback_query.message.answer(f"✍️ Введите название этажа")

@router.message(F.text, AdminStates.create_floor_name)
async def floor_create_photo(message: Message, state: FSMContext):
    await state.update_data({'floor_name': message.text})
    await state.set_state(AdminStates.create_floor_photo)
    await message.answer(f"✍️ Отправьте фото")

@router.message(F.photo, AdminStates.create_floor_photo)
async def floor_create(message: Message, state: FSMContext):
    try:
        image_path = f'{settings.IMAGES_PATH}\\map\\floors\\{message.photo[-1].file_id}.png'
        await message.bot.download(file=message.photo[-1].file_id,destination= image_path)
        building_id = (await state.get_data())['building'].id
        floor = Floor(name=(await state.get_data())['floor_name'],photo_path=image_path,building_id=building_id)
        data_state = MapsDbBl.create_floor(floor)
        if isinstance(data_state, DataSuccess):
            floor_id = data_state.data
            await floor_selection(state,message=message, building_id=building_id,floor_id=floor_id)
        else:
            await message.answer(f'❌ {data_state.error_message}')
    except Exception as ex:
        logger.exception(ex)
        await message.answer(f'❌ Ошибка отправки сообщения!')

@router.callback_query(F.data == 'delete_floor')
async def delete_floor_button(callback_query: types.CallbackQuery, state: FSMContext):
    floor = (await state.get_data())['floor']
    data_state = MapsDbBl.delete_floor(floor)
    if isinstance(data_state, DataSuccess):
        building_id = (await state.get_data())['building'].id
        await floors_button(state, message=callback_query.message, building_id=building_id)
    else:
        await callback_query.message.answer(f'❌ {data_state.error_message}')

@router.callback_query(F.data == "create_section")
async def section_create_name(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(AdminStates.create_section_name)
    await callback_query.message.answer(f"✍️ Введите название отдела")

@router.message(F.text, AdminStates.create_section_name)
async def section_create_photo(message: Message, state: FSMContext):
    await state.update_data({'section_name': message.text})
    await state.set_state(AdminStates.create_section_photo)
    await message.answer(f"✍️ Отправьте фото")

@router.message(F.photo, AdminStates.create_section_photo)
async def section_create(message: Message, state: FSMContext):
    try:
        image_path = f'{settings.IMAGES_PATH}\\map\\sections\\{message.photo[-1].file_id}.png'
        await message.bot.download(file=message.photo[-1].file_id,destination= image_path)
        floor_id = (await state.get_data())['floor'].id
        building_id = (await state.get_data())['building'].id
        section = Section(name=(await state.get_data())['section_name'],photo_path=image_path,floor_id=floor_id)
        data_state = MapsDbBl.create_section(section)
        if isinstance(data_state, DataSuccess):
            section_id = data_state.data
            await section_selection(state,message=message, building_id=building_id,floor_id=floor_id,section_id=section_id)
        else:
            await message.answer(f'❌ {data_state.error_message}')
    except Exception as ex:
        logger.exception(ex)
        await message.answer(f'❌ Ошибка отправки сообщения!')

@router.callback_query(F.data == 'delete_section')
async def delete_section_button(callback_query: types.CallbackQuery, state: FSMContext):
    section = (await state.get_data())['section']
    data_state = MapsDbBl.delete_section(section)
    if isinstance(data_state, DataSuccess):
        floor_id = (await state.get_data())['floor'].id
        building_id = (await state.get_data())['building'].id
        await floor_selection(state, message=callback_query.message, floor_id=floor_id,building_id=building_id)
    else:
        await callback_query.message.answer(f'❌ {data_state.error_message}')

@router.callback_query(F.data == 'change_building_name')
async def change_building_name(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(AdminStates.change_building_name)
    await callback_query.message.answer(f"✍️ Введите новое название")


@router.message(F.text, AdminStates.change_building_name)
async def changed_building_name(message: Message, state: FSMContext):
    building = (await state.get_data())['building']
    building.name = message.text
    data_state = MapsDbBl.update_building(building)

    if isinstance(data_state, DataSuccess):
        await floors_button(state, message=message, building_id=building.id)
    else:
        await message.answer(f'❌ {data_state.error_message}')

@router.callback_query(F.data == 'change_building_photo')
async def change_building_photo(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(AdminStates.change_building_photo)
    await callback_query.message.answer(f"✍️ Отправьте новое фото")


@router.message(F.photo, AdminStates.change_building_photo)
async def changed_building_photo(message: Message, state: FSMContext):
    building = (await state.get_data())['building']
    old_image_path = building.photo_path
    image_path = f'{settings.IMAGES_PATH}\\map\\buildings\\{message.photo[-1].file_id}.png'
    await message.bot.download(file=message.photo[-1].file_id, destination=image_path)
    building.photo_path = image_path
    data_state = MapsDbBl.update_building(building)

    if isinstance(data_state, DataSuccess):
        if os.path.exists(old_image_path): # это должно быть в bl слое, но так-как на обновление картинки и названия один запрос, мне лень было модифицировать и сделал так, но вам лучше так не делать)
            os.remove(old_image_path)

        await floors_button(state, message=message, building_id=building.id)
    else:
        await message.answer(f'❌ {data_state.error_message}')

@router.callback_query(F.data == 'change_floor_name')
async def change_floor_name(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(AdminStates.change_floor_name)
    await callback_query.message.answer(f"✍️ Введите новое название")


@router.message(F.text, AdminStates.change_floor_name)
async def changed_floor_name(message: Message, state: FSMContext):
    floor = (await state.get_data())['floor']
    floor.name = message.text
    data_state = MapsDbBl.update_floor(floor)

    if isinstance(data_state, DataSuccess):
        await floor_selection(state, message=message, building_id=floor.building_id,floor_id=floor.id)
    else:
        await message.answer(f'❌ {data_state.error_message}')

@router.callback_query(F.data == 'change_floor_photo')
async def change_floor_photo(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(AdminStates.change_floor_photo)
    await callback_query.message.answer(f"✍️ Отправьте новое фото")


@router.message(F.photo, AdminStates.change_floor_photo)
async def changed_floor_photo(message: Message, state: FSMContext):
    floor = (await state.get_data())['floor']
    old_image_path = floor.photo_path
    image_path = f'{settings.IMAGES_PATH}\\map\\floors\\{message.photo[-1].file_id}.png'
    await message.bot.download(file=message.photo[-1].file_id, destination=image_path)
    floor.photo_path = image_path
    data_state = MapsDbBl.update_floor(floor)

    if isinstance(data_state, DataSuccess):
        if os.path.exists(old_image_path): # это должно быть в bl слое, но так-как на обновление картинки и названия один запрос, мне лень было модифицировать и сделал так, но вам лучше так не делать)
            os.remove(old_image_path)

        await floor_selection(state, message=message, building_id=floor.building_id,floor_id=floor.id)
    else:
        await message.answer(f'❌ {data_state.error_message}')

@router.callback_query(F.data == 'change_section_name')
async def change_section_name(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(AdminStates.change_section_name)
    await callback_query.message.answer(f"✍️ Введите новое название")


@router.message(F.text, AdminStates.change_section_name)
async def changed_section_name(message: Message, state: FSMContext):
    section = (await state.get_data())['section']
    section.name = message.text
    data_state = MapsDbBl.update_section(section)

    if isinstance(data_state, DataSuccess):
        building_id = (await state.get_data())['building'].id
        await section_selection(state, message=message, building_id=building_id,floor_id=section.floor_id,section_id=section.id)
    else:
        await message.answer(f'❌ {data_state.error_message}')

@router.callback_query(F.data == 'change_section_photo')
async def change_section_photo(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(AdminStates.change_section_photo)
    await callback_query.message.answer(f"✍️ Отправьте новое фото")


@router.message(F.photo, AdminStates.change_section_photo)
async def changed_section_photo(message: Message, state: FSMContext):
    section = (await state.get_data())['section']
    old_image_path = section.photo_path
    image_path = f'{settings.IMAGES_PATH}\\map\\sections\\{message.photo[-1].file_id}.png'
    await message.bot.download(file=message.photo[-1].file_id, destination=image_path)
    section.photo_path = image_path
    data_state = MapsDbBl.update_section(section)

    if isinstance(data_state, DataSuccess):
        if os.path.exists(old_image_path): # это должно быть в bl слое, но так-как на обновление картинки и названия один запрос, мне лень было модифицировать и сделал так, но вам лучше так не делать)
            os.remove(old_image_path)

        building_id = (await state.get_data())['building'].id
        await section_selection(state, message=message, building_id=building_id,floor_id=section.floor_id,section_id=section.id)
    else:
        await message.answer(f'❌ {data_state.error_message}')