from aiogram import Router, types, F
from aiogram.types import FSInputFile, InputMediaPhoto
from .keyboards import get_buildings_keyboard, get_floors_keyboard, get_sections_keyboard
from .keyboards import BuildingCallbackFactory, FloorCallbackFactory, SectionCallbackFactory, BackCallbackFactory, BackToBuildingCallbackFactory
from .keyboards import buildings, floors, sections

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
    building = next(b for b in buildings if b["id"] == building_id)

    # Отправляем фото здания
    media = InputMediaPhoto(
        media=FSInputFile(building["image"]),
        caption=f"Вы выбрали здание: {building['name']}"
    )
    await callback_query.message.edit_media(
        media=media,
        reply_markup=get_floors_keyboard(building_id=building_id)
    )

# Обработчик выбора этажа
@router.callback_query(FloorCallbackFactory.filter())
async def handle_floor_selection(callback_query: types.CallbackQuery, callback_data: FloorCallbackFactory):
    building_id = callback_data.building_id
    floor_id = callback_data.floor_id
    floor = next(f for f in floors[building_id] if f["id"] == floor_id)

    # Отправляем схему этажа
    media = InputMediaPhoto(
        media=FSInputFile(floor["image"]),
        caption=f"Вы выбрали этаж: {floor['name']}"
    )
    await callback_query.message.edit_media(
        media=media,
        reply_markup=get_sections_keyboard(building_id=building_id, floor_id=floor_id)
    )

# Обработчик выбора раздела
@router.callback_query(SectionCallbackFactory.filter())
async def handle_section_selection(callback_query: types.CallbackQuery, callback_data: SectionCallbackFactory):
    building_id = callback_data.building_id
    floor_id = callback_data.floor_id
    section_id = callback_data.section_id
    section = next(s for s in sections[(building_id, floor_id)] if s["id"] == section_id)

    # Отправляем схему этажа с выделенным разделом
    media = InputMediaPhoto(
        media=FSInputFile(floors[building_id][floor_id - 1]["image"]),  # Используем ту же схему этажа
        caption=f"Вы выбрали раздел: {section['name']}"
    )
    await callback_query.message.edit_media(
        media=media,
        reply_markup=get_sections_keyboard(building_id=building_id, floor_id=floor_id)
    )

# Обработчик кнопки "Назад"
@router.callback_query(BackCallbackFactory.filter())
async def handle_back_button(callback_query: types.CallbackQuery, callback_data: BackCallbackFactory):
    # Возвращаемся к выбору этажей
    building_id = callback_data.building_id
    building = next(b for b in buildings if b["id"] == building_id)

    # Отправляем фото здания
    media = InputMediaPhoto(
        media=FSInputFile(building["image"]),
        caption=f"Вы выбрали здание: {building['name']}"
    )
    await callback_query.message.edit_media(
        media=media,
        reply_markup=get_floors_keyboard(building_id=building_id)
    )

@router.callback_query(BackToBuildingCallbackFactory.filter())
async def handle_back_button(callback_query: types.CallbackQuery, callback_data: BackToBuildingCallbackFactory):
    # Возвращаемся к выбору зданий
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