from aiogram.utils.keyboard import InlineKeyboardBuilder
from application.tg_bot.office_maps.admin_actions.keyboards import AdminFloorCallbackFactory
from domain.office_maps.db_bl import MapsDbBl
from utils.data_state import DataSuccess

def get_floors_keyboard(building_id: int):
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Добавить этаж",
        callback_data='create_floor'
    )
    builder.button(
        text="Изменить название",
        callback_data='change_building_name'
    )
    builder.button(
        text="Изменить фото",
        callback_data='change_building_photo'
    )
    builder.button(
        text="Удалить здание",
        callback_data='delete_building'
    )
    # Получаем список этажей для конкретного здания
    data_state = MapsDbBl.get_floors_by_building(building_id)
    if isinstance(data_state, DataSuccess):
        for floor in data_state.data:
            builder.button(
                text=floor.name,
                callback_data=AdminFloorCallbackFactory(building_id=building_id, floor_id=floor.id)
            )
    else:
        # Если данные не получены, можно добавить кнопку с сообщением об ошибке
        builder.button(text="Ошибка загрузки этажей", callback_data="error")

    builder.button(
        text="🔙 Назад к зданиям",
        callback_data='office_maps_button_admin'
    )
    builder.button(
        text="🔙 Назад в меню",
        callback_data='back_to_admin_main_menu'
    )
    builder.adjust(1,3,1)
    return builder.as_markup()
