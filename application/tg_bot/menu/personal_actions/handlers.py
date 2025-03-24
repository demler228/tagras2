from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from application.tg_bot.filters.is_admin import is_admin
from application.tg_bot.menu.personal_actions.keyboards.menu_keyboard import get_main_menu_keyboard

router = Router()
router.message.filter(F.chat.type == "private")

@router.message(CommandStart())
async def start_handler(message: types.Message):
    print(message.from_user.id)
    await message.answer("Привет! Я бот для адаптации сотрудников. Выберите, чем я могу помочь!", reply_markup=get_main_menu_keyboard(is_admin(message.from_user.id)))

@router.callback_query(F.data == "back_to_main_menu" )
async def back_handler(callback_query: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback_query.message.delete()
    await callback_query.message.answer("Вы вернулись в главное меню!",
                                       reply_markup=get_main_menu_keyboard(is_admin(callback_query.from_user.id)))