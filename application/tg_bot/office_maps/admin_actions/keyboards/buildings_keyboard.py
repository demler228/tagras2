from aiogram.utils.keyboard import InlineKeyboardBuilder
from application.tg_bot.office_maps.admin_actions.keyboards import AdminBuildingCallbackFactory
from domain.office_maps.db_bl import MapsDbBl
from utils.data_state import DataSuccess

def get_buildings_keyboard():
    builder = InlineKeyboardBuilder()

    builder.button(
        text="🔙Добавить здание",
        callback_data='create_building'
    )
    # Получаем список зданий из базы данных
    data_state = MapsDbBl.get_buildings()
    if isinstance(data_state, DataSuccess):
        for building in data_state.data:
            builder.button(
                text=building.name,
                callback_data=AdminBuildingCallbackFactory(building_id=building.id)
            )
    else:
        # Если данные не получены, можно добавить кнопку с сообщением об ошибке
        builder.button(text="Ошибка загрузки зданий", callback_data="error")

    builder.button(
        text="🔙 Назад в меню",
        callback_data='back_to_admin_main_menu'
    )
    builder.adjust(1)
    return builder.as_markup()
