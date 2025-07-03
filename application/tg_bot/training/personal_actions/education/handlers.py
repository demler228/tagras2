import os

from aiogram import Router, types, F
from aiogram.types import FSInputFile

from application.tg_bot.menu.personal_actions.keyboards.menu_keyboard import  get_main_menu_keyboard
from .keyboards.education_themes_keyboard import get_themes_keyboard, get_materials_keyboard, ThemeCallback
from domain.training.education.db_bl import EducationBL


router = Router()


@router.callback_query(F.data == "education_button")
async def handle_education_button(callback_query: types.CallbackQuery):
    data_state = EducationBL.get_themes()
    await callback_query.message.edit_text(
        "Выберите тему:",
        reply_markup=get_themes_keyboard(data_state.data)
    )


@router.callback_query(ThemeCallback.filter(F.action == "select"))
async def show_materials(callback_query: types.CallbackQuery, callback_data: ThemeCallback):
    await callback_query.answer()

    data_state = EducationBL.get_materials(callback_data.theme_id)
    materials = data_state.data

    if not materials:
        await callback_query.message.answer("Материалы не найдены по выбранной теме.")
    else:
        await callback_query.message.answer("<b>Материалы по теме:</b>", parse_mode="HTML")

        for material in materials:
            file_path = material.url.replace("\\", "/")  # на случай, если в базе путь с `\`
            file_path = os.path.join("temp_files", os.path.basename(file_path))

            if not os.path.exists(file_path):
                await callback_query.message.answer(f"Файл не найден: {material.title}")
                continue

            file = FSInputFile(file_path)
            ext = os.path.splitext(file_path)[1].lower()

            try:
                if ext == ".pdf":
                    await callback_query.message.answer_document(file, caption=material.title)
                elif ext in [".mp4", ".mov", ".avi", ".mkv"]:
                    await callback_query.message.answer_video(file, caption=material.title)
                else:
                    await callback_query.message.answer_document(file, caption=material.title)
            except Exception as e:
                await callback_query.message.answer(f"Не удалось отправить файл: {material.title}")

    await callback_query.message.answer(
        "Выберите действие:",
        reply_markup=get_materials_keyboard(callback_data.theme_id)
    )


@router.callback_query(ThemeCallback.filter(F.action == "back"))
async def back_to_themes(callback_query: types.CallbackQuery):
    data_state = EducationBL.get_themes()
    await callback_query.message.edit_text(
        "Выберите тему:",
        reply_markup=get_themes_keyboard(data_state.data)
    )


@router.callback_query(F.data == "back_to_menu")
async def back_to_menu(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(
        "Главное меню:",
        reply_markup=get_main_menu_keyboard()
    )
