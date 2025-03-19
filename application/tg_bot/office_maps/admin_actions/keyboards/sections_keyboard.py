from aiogram.utils.keyboard import InlineKeyboardBuilder
from application.tg_bot.office_maps.admin_actions.keyboards import AdminSectionCallbackFactory, \
    AdminBuildingCallbackFactory
from domain.office_maps.db_bl import MapsDbBl
from utils.data_state import DataSuccess

def get_sections_keyboard(building_id: int, floor_id: int):
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Добавить отдел",
        callback_data='create_section'
    )
    builder.button(
        text="Изменить название",
        callback_data='change_floor_name'
    )
    builder.button(
        text="Изменить фото",
        callback_data='change_floor_photo'
    )
    builder.button(
        text="Удалить этаж",
        callback_data='delete_floor'
    )
    # Получаем список разделов для конкретного этажа
    data_state = MapsDbBl.get_sections_by_floor(floor_id)
    if isinstance(data_state, DataSuccess):
        sections = data_state.data
        for section in sections:
            builder.button(
                text=section.name,
                callback_data=AdminSectionCallbackFactory(building_id=building_id, floor_id=floor_id, section_id=section.id)
            )
    else:
        # Если данные не получены, можно добавить кнопку с сообщением об ошибке
        builder.button(text="Ошибка загрузки разделов", callback_data="error")

    # Кнопка "Назад к зданиям"
    builder.button(
        text="🔙 Назад к этажам",
        callback_data=AdminBuildingCallbackFactory(building_id=building_id)
    )

    # Кнопка "Назад в меню"
    builder.button(
        text="🔙 Назад в меню",
        callback_data='back_to_admin_main_menu'
    )

    builder.adjust(1,3,1)
    return builder.as_markup()