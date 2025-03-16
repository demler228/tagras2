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

@router.callback_query(BuildingCallbackFactory.filter())
async def handle_building_selection(callback_query: types.CallbackQuery, callback_data: BuildingCallbackFactory):
    building_id = callback_data.building_id
    data_state = BuildingDbBl.get_buildings()  # Получаем список всех зданий
    if isinstance(data_state, DataSuccess):
        buildings = data_state.data
        # Ищем здание по ID
        building = next((b for b in buildings if b.id == building_id), None)
        if building:
            # Отправляем фото здания с его именем
            media = InputMediaPhoto(
                media=FSInputFile(building.photo_path),
                caption=f"Вы выбрали здание: {building.name}"  # Используем имя здания
            )
            await callback_query.message.edit_media(
                media=media,
                reply_markup=get_floors_keyboard(building_id=building_id)
            )
        else:
            await callback_query.message.answer("Здание не найдено.")
    else:
        await callback_query.message.answer(data_state.message)

@router.callback_query(FloorCallbackFactory.filter())
async def handle_floor_selection(callback_query: types.CallbackQuery, callback_data: FloorCallbackFactory):
    floor_id = callback_data.floor_id
    building_id = callback_data.building_id
    data_state = FloorDbBl.get_floors_by_building(building_id)  # Получаем список этажей для здания
    if isinstance(data_state, DataSuccess):
        floors = data_state.data
        # Ищем этаж по ID
        floor = next((f for f in floors if f.id == floor_id), None)
        if floor:
            # Отправляем фото этажа с его именем
            media = InputMediaPhoto(
                media=FSInputFile(floor.photo_path),
                caption=f"Вы выбрали этаж: {floor.name}"  # Используем имя этажа
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
async def handle_section_selection(callback_query: types.CallbackQuery, callback_data: SectionCallbackFactory):
    section_id = callback_data.section_id
    floor_id = callback_data.floor_id
    building_id = callback_data.building_id
    data_state = SectionDbBl.get_sections_by_floor(floor_id)  # Получаем список разделов для этажа
    if isinstance(data_state, DataSuccess):
        sections = data_state.data
        # Ищем раздел по ID
        section = next((s for s in sections if s.id == section_id), None)
        if section:
            # Отправляем фото раздела с его именем
            media = InputMediaPhoto(
                media=FSInputFile(section.photo_path),
                caption=f"Вы выбрали раздел: {section.name}"  # Используем имя раздела
            )
            await callback_query.message.edit_media(
                media=media,
                reply_markup=get_sections_keyboard(building_id=building_id, floor_id=floor_id)
            )
        else:
            await callback_query.message.answer("Раздел не найден.")
    else:
        await callback_query.message.answer(data_state.message)

@router.callback_query(BackCallbackFactory.filter())
async def handle_back_button(callback_query: types.CallbackQuery, callback_data: BackCallbackFactory):
    building_id = callback_data.building_id
    data_state = BuildingDbBl.get_buildings()  # Получаем список всех зданий
    if isinstance(data_state, DataSuccess):
        buildings = data_state.data
        # Ищем здание по ID
        building = next((b for b in buildings if b.id == building_id), None)
        if building:
            # Отправляем фото здания с его именем
            media = InputMediaPhoto(
                media=FSInputFile(building.photo_path),
                caption=f"Вы выбрали здание: {building.name}"  # Используем имя здания
            )
            await callback_query.message.edit_media(
                media=media,
                reply_markup=get_floors_keyboard(building_id=building_id)
            )
        else:
            await callback_query.message.answer("Здание не найдено.")
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