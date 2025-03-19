from aiogram import Router, types, F
from aiogram.filters import CommandStart

from application.tg_bot.menu.personal_actions.keyboards.menu_keyboard import get_main_menu_keyboard

router = Router()
router.message.filter(F.chat.type == "private")

@router.message(CommandStart())
async def start_handler(message: types.Message):
    print(message.from_user.id)
    await message.answer("Привет! Я бот для адаптации сотрудников. Выберите, чем я могу помочь!", reply_markup=get_main_menu_keyboard())