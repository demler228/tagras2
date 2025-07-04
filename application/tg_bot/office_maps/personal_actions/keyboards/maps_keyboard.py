from aiogram.utils.keyboard import InlineKeyboardBuilder
from application.tg_bot.office_maps.personal_actions.keyboards.callback_factories import BackToSectionCallbackFactory
from domain.office_maps.db_bl import MapsDbBl

from .callback_factories import (
    BuildingCallbackFactory,
    FloorCallbackFactory,
    SectionCallbackFactory,
    BackToBuildingCallbackFactory,
    BackToFloorCallbackFactory,
    BackToSectionCallbackFactory,
)
from application.tg_bot.faq.personal_actions.keyboards import BackToMenuCallbackFactory
from utils.data_state import DataSuccess


def get_buildings_keyboard():
    builder = InlineKeyboardBuilder()

    # Получаем список зданий из базы данных
    data_state = MapsDbBl.get_buildings()
    if isinstance(data_state, DataSuccess):
        for building in data_state.data:
            builder.button(
                text=building.name,
                callback_data=BuildingCallbackFactory(building_id=building.id)
            )
    else:
        # Если данные не получены, можно добавить кнопку с сообщением об ошибке
        builder.button(text="Ошибка загрузки зданий", callback_data="error")

    builder.button(
        text="🔙 Назад в меню",
        callback_data=BackToMenuCallbackFactory()
    )
    builder.adjust(1)
    return builder.as_markup()


def get_floors_keyboard(building_id: int):
    builder = InlineKeyboardBuilder()

    # Получаем список этажей для конкретного здания
    data_state = MapsDbBl.get_floors_by_building(building_id)
    if isinstance(data_state, DataSuccess):
        for floor in data_state.data:
            builder.button(
                text=floor.name,
                callback_data=FloorCallbackFactory(building_id=building_id, floor_id=floor.id)
            )
    else:
        # Если данные не получены, можно добавить кнопку с сообщением об ошибке
        builder.button(text="Ошибка загрузки этажей", callback_data="error")

    builder.button(
        text="🔙 Назад к зданиям",
        callback_data=BackToBuildingCallbackFactory()
    )
    builder.button(
        text="🔙 Назад в меню",
        callback_data=BackToMenuCallbackFactory()
    )
    builder.adjust(1)
    return builder.as_markup()


def get_sections_keyboard(building_id: int, floor_id: int):
    builder = InlineKeyboardBuilder()

    # Получаем список разделов для конкретного этажа
    data_state = MapsDbBl.get_sections_by_floor(floor_id)
    if isinstance(data_state, DataSuccess):
        sections = data_state.data
        for section in sections:
            builder.button(
                text=section.name,
                callback_data=SectionCallbackFactory(building_id=building_id, floor_id=floor_id, section_id=section.id)
            )
    else:
        # Если данные не получены, можно добавить кнопку с сообщением об ошибке
        builder.button(text="Ошибка загрузки разделов", callback_data="error")

    # Кнопка "Назад к зданиям"
    builder.button(
        text="🔙 Назад к этажам",
        callback_data=BackToFloorCallbackFactory(building_id=building_id)
    )

    # Кнопка "Назад в меню"
    builder.button(
        text="🔙 Назад в меню",
        callback_data=BackToMenuCallbackFactory()
    )

    builder.adjust(1)
    return builder.as_markup()

def get_section_keyboard(building_id: int, floor_id: int):
    builder = InlineKeyboardBuilder()

    # Кнопка "Назад к этажам"
    builder.button(
        text="🔙 Назад к отделам",
        callback_data=BackToSectionCallbackFactory(building_id=building_id, floor_id=floor_id)
    )

    # Кнопка "Назад в меню"
    builder.button(
        text="🔙 Назад в меню",
        callback_data=BackToMenuCallbackFactory()
    )

    builder.adjust(1)
    return builder.as_markup()