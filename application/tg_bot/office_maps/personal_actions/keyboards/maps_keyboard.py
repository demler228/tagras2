from aiogram.utils.keyboard import InlineKeyboardBuilder
from .callback_factories import BuildingCallbackFactory, FloorCallbackFactory, SectionCallbackFactory, BackCallbackFactory, BackToBuildingCallbackFactory
from .data_stubs import buildings, floors, sections
from application.tg_bot.faq.personal_actions.keyboards.callback_factories import BackToMenuCallbackFactory

def get_buildings_keyboard():
    builder = InlineKeyboardBuilder()
    for building in buildings:
        builder.button(
            text=building["name"],
            callback_data=BuildingCallbackFactory(building_id=building["id"])
        )
    builder.button(
        text="🔙 Назад в меню",
        callback_data=BackToMenuCallbackFactory()
    )
    builder.adjust(1)
    return builder.as_markup()

def get_floors_keyboard(building_id: int):
    builder = InlineKeyboardBuilder()
    for floor in floors[building_id]:
        builder.button(
            text=floor["name"],
            callback_data=FloorCallbackFactory(building_id=building_id, floor_id=floor["id"])
        )
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
    for section in sections[(building_id, floor_id)]:
        builder.button(
            text=section["name"],
            callback_data=SectionCallbackFactory(building_id=building_id, floor_id=floor_id, section_id=section["id"])
        )
    builder.button(
        text="🔙 Назад к этажам",
        callback_data=BackCallbackFactory(action="to_floors", building_id=building_id)
    )
    builder.button(
        text="🔙 Назад в меню",
        callback_data=BackToMenuCallbackFactory()
    )
    builder.adjust(1)
    return builder.as_markup()