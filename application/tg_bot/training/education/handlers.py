from aiogram import Router, types, F

from .keyboards.education_themes_keyboard import get_themes_keyboard
from domain.training.education.bl_models import EducationBL
from .keyboards.education_themes_keyboard import ThemeCallback


router = Router()

@router.callback_query(F.data == "education_button")
async def handle_education_button(callback_query: types.CallbackQuery):
    themes = EducationBL.get_themes()
    await callback_query.message.answer("Выбери тему:", reply_markup=get_themes_keyboard(themes))

@router.callback_query(ThemeCallback.filter())
async def show_materials(callback_query: types.CallbackQuery, callback_data: ThemeCallback):
    materials = EducationBL.get_materials(callback_data.theme_id)
    content = "\n".join(f"{material[0]} {material[1]}" for material in materials)

    await callback_query.message.answer(content)
