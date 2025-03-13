from aiogram import Router, types, F
from aiogram.types import FSInputFile, InputMediaPhoto

from .keyboards import get_office_maps_keyboard, get_office_map_keyboard

router = Router()


# Обработчик кнопки "Карта офиса"
@router.callback_query(F.data == "office_maps_button")
async def handle_office_maps_button(callback_query: types.CallbackQuery):
    """
    Обрабатывает нажатие на кнопку "Карта офиса".
    """
    await callback_query.message.answer(
        "Выберите этаж:",
        reply_markup=get_office_maps_keyboard()
    )


# Обработчик выбора этажа
@router.callback_query(F.data.startswith("office_map_"))
async def handle_office_map_floor(callback_query: types.CallbackQuery):
    """
    Обрабатывает выбор этажа и отображает карту.
    """
    data = callback_query.data.split("_")
    floor = data[2]  # Получаем номер этажа из callback_data

    map_image_path = r"C:\Users\ratmi\PycharmProjects\employee_adaptation_project\application\tg_bot\office_maps\personal_actions\floor.png"

    # Проверяем, существует ли файл
    import os
    if not os.path.exists(map_image_path):
        await callback_query.message.answer("Карта этажа не найдена.")
        return

    # Создаем объект InputMediaPhoto для замены сообщения
    media = InputMediaPhoto(
        media=FSInputFile(map_image_path),  # Используем FSInputFile для локальных файлов
        caption=f"Карта {floor} этажа"
    )

    # Заменяем старое сообщение на новое с фотографией
    await callback_query.message.edit_media(
        media=media,
        reply_markup=get_office_map_keyboard(floor)
    )


@router.callback_query(F.data == "back_to_floors")
async def back_to_floors_handler(callback_query: types.CallbackQuery):
    """
    Возвращает пользователя к выбору этажа.
    """
    # Проверяем, есть ли в сообщении медиа (фото)
    if callback_query.message.photo:
        # Если сообщение содержит фото, заменяем его на текстовое сообщение
        await callback_query.message.delete()  # Удаляем старое сообщение с фото
        await callback_query.message.answer(
            "Выберите этаж:",
            reply_markup=get_office_maps_keyboard()
        )
    else:
        # Если сообщение текстовое, просто редактируем его
        await callback_query.message.edit_text(
            "Выберите этаж:",
            reply_markup=get_office_maps_keyboard()
        )


# Обработчик кнопки "В меню"
@router.callback_query(F.data == "back_to_menu")
async def back_to_menu_handler(callback_query: types.CallbackQuery):
    """
    Удаляет все сообщения, кроме меню.
    """
    # Удаляем текущее сообщение
    await callback_query.message.delete()
