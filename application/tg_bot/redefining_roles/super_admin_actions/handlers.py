from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from loguru import logger
from application.tg_bot.filters.is_admin import IsAdminFilter
from application.tg_bot.filters.is_admin import is_super_admin
from application.tg_bot.menu.admin_actions.keyboards.menu_keyboard import get_admin_main_menu_keyboard

router = Router()


@router.callback_query(F.data == "redefining_roles_super_admin")
async def redefining_roles_handler(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(
        "Вы в разделе переопределения ролей:"
    )