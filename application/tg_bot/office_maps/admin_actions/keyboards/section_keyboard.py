from aiogram.utils.keyboard import InlineKeyboardBuilder
from .callback_factories import (
    AdminFloorCallbackFactory,
)

def get_section_keyboard(building_id: int, floor_id: int):
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Изменить название",
        callback_data='change_section_name'
    )
    builder.button(
        text="Изменить фото",
        callback_data='change_section_photo'
    )
    builder.button(
        text="Удалить отдел",
        callback_data='delete_section'
    )
    # Кнопка "Назад к этажам"
    builder.button(
        text="🔙 Назад к отделам",
        callback_data=AdminFloorCallbackFactory(building_id=building_id, floor_id=floor_id)
    )

    # Кнопка "Назад в меню"
    builder.button(
        text="🔙 Назад в меню",
        callback_data='back_to_admin_main_menu'
    )

    builder.adjust(3,1)
    return builder.as_markup()