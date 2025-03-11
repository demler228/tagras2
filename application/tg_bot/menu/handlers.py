from aiogram import Router, types
from aiogram.filters import CommandStart

from .keyboards.menu_keyboard import get_main_menu_keyboard

router = Router()

@router.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer("Привет! Я бот для адаптации сотрудников. Выберите, чем я могу помочь!", reply_markup=get_main_menu_keyboard())