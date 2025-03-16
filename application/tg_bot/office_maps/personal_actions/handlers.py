from aiogram import Router, types, F
from aiogram.types import FSInputFile, InputMediaPhoto
from .keyboards import get_buildings_keyboard, get_floors_keyboard, get_sections_keyboard
from .keyboards import (
    BuildingCallbackFactory,
    FloorCallbackFactory,
    SectionCallbackFactory,
    BackCallbackFactory,
    BackToBuildingCallbackFactory,
)
from domain.office_maps.db_bl import BuildingDbBl, FloorDbBl, SectionDbBl
from utils.data_state import DataSuccess

router = Router()

# Обработчик кнопки "Карта офиса"
@router.callback_query(F.data == "office_maps_button")
async def handle_office_maps_button(callback_query: types.CallbackQuery):
    await callback_query.message.answer(
        "Выберите здание:",
        reply_markup=get_buildings_keyboard()
    )

# Обработчик выбора здания
@router.callback_query(BuildingCallbackFactory.filter())
async def handle_building_selection(callback_query: types.CallbackQuery, callback_data: BuildingCallbackFactory):
    building_id = callback_data.building_id
    data_state = BuildingDbBl.get_building_photo(building_id)
    if isinstance(data_state, DataSuccess):
        photo_path = data_state.data
        # Отправляем фото здания
        media = InputMediaPhoto(
            media=FSInputFile(photo_path),
            caption=f"Вы выбрали здание: {callback_data.building_id}"
        )
        await callback_query.message.edit_media(
            media=media,
            reply_markup=get_floors_keyboard(building_id=building_id)
        )
    else:
        await callback_query.message.answer(data_state.message)

# Обработчик выбора этажа
@router.callback_query(FloorCallbackFactory.filter())
async def handle_floor_selection(callback_query: types.CallbackQuery, callback_data: FloorCallbackFactory):
    floor_id = callback_data.floor_id
    data_state = FloorDbBl.get_floor_photo(floor_id)
    if isinstance(data_state, DataSuccess):
        photo_path = data_state.data
        # Отправляем фото этажа
        media = InputMediaPhoto(
            media=FSInputFile(photo_path),
            caption=f"Вы выбрали этаж: {callback_data.floor_id}"
        )
        await callback_query.message.edit_media(
            media=media,
            reply_markup=get_sections_keyboard(building_id=callback_data.building_id, floor_id=floor_id)
        )
    else:
        await callback_query.message.answer(data_state.message)

# Обработчик выбора раздела
@router.callback_query(SectionCallbackFactory.filter())
async def handle_section_selection(callback_query: types.CallbackQuery, callback_data: SectionCallbackFactory):
    section_id = callback_data.section_id
    data_state = SectionDbBl.get_section_photo(section_id)
    if isinstance(data_state, DataSuccess):
        photo_path = data_state.data
        # Отправляем фото раздела
        media = InputMediaPhoto(
            media=FSInputFile(photo_path),
            caption=f"Вы выбрали раздел: {callback_data.section_id}"
        )
        await callback_query.message.edit_media(
            media=media,
            reply_markup=get_sections_keyboard(building_id=callback_data.building_id, floor_id=callback_data.floor_id)
        )
    else:
        await callback_query.message.answer(data_state.message)

# Обработчик кнопки "Назад"
@router.callback_query(BackCallbackFactory.filter())
async def handle_back_button(callback_query: types.CallbackQuery, callback_data: BackCallbackFactory):
    building_id = callback_data.building_id
    data_state = BuildingDbBl.get_building_photo(building_id)
    if isinstance(data_state, DataSuccess):
        photo_path = data_state.data
        # Отправляем фото здания
        media = InputMediaPhoto(
            media=FSInputFile(photo_path),
            caption=f"Вы выбрали здание: {building_id}"
        )
        await callback_query.message.edit_media(
            media=media,
            reply_markup=get_floors_keyboard(building_id=building_id)
        )
    else:
        await callback_query.message.answer(data_state.message)

@router.callback_query(BackToBuildingCallbackFactory.filter())
async def handle_back_button(callback_query: types.CallbackQuery, callback_data: BackToBuildingCallbackFactory):
    if callback_query.message.photo:
        await callback_query.message.delete()
        await callback_query.message.answer(
            "Выберите здание:",
            reply_markup=get_buildings_keyboard()
        )
    else:
        await callback_query.message.edit_text(
            "Выберите здание:",
            reply_markup=get_buildings_keyboard()
        )