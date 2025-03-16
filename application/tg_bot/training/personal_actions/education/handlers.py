from aiogram import Router, types, F

from application.tg_bot.menu.personal_actions.keyboards.menu_keyboard import  get_main_menu_keyboard
from .keyboards.education_themes_keyboard import get_themes_keyboard, get_materials_keyboard, ThemeCallback
from domain.training.education.bl_models import EducationBL


router = Router()


@router.callback_query(F.data == "education_button")
async def handle_education_button(callback_query: types.CallbackQuery):
    data_state = EducationBL.get_themes()
    await callback_query.message.edit_text(
        "Выбери тему:",
        reply_markup=get_themes_keyboard(data_state.data)
    )


@router.callback_query(ThemeCallback.filter(F.action == "select"))
async def show_materials(callback_query: types.CallbackQuery, callback_data: ThemeCallback):
    data_state = EducationBL.get_materials(callback_data.theme_id)
    materials = data_state.data
    content = "\n".join(f"{material.title} {material.url}" for material in materials)

    await callback_query.message.edit_text(
        f"<b>Материалы по теме:</b>\n\n{content}",
        reply_markup=get_materials_keyboard(callback_data.theme_id),
        parse_mode="HTML"
    )


@router.callback_query(ThemeCallback.filter(F.action == "back"))
async def back_to_themes(callback_query: types.CallbackQuery):
    data_state = EducationBL.get_themes()
    await callback_query.message.edit_text(
        "Выбери тему:",
        reply_markup=get_themes_keyboard(data_state.data)
    )


@router.callback_query(F.data == "back_to_menu")
async def back_to_menu(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(
        "Главное меню:",
        reply_markup=get_main_menu_keyboard()
    )
