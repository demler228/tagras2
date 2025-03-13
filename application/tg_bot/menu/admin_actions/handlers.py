from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from application.tg_bot.filters.is_admin import IsAdminFilter
from application.tg_bot.menu.admin_actions.keyboards.menu_keyboard import get_admin_main_menu_keyboard


router = Router()
router.message.filter(F.chat.type == "private", IsAdminFilter()) # allow bot admin actions only for bot owner

@router.message(CommandStart())
async def start_handler(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Привет! Вы в админ панели, что хотите изменить?", reply_markup=get_admin_main_menu_keyboard())

@router.callback_query(F.data == "back_to_admin_main_menu")
async def back_handler(callback_query: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback_query.message.delete()
    await callback_query.message.answer("Вы вернулись в главное меню!",
                                       reply_markup=get_admin_main_menu_keyboard())

