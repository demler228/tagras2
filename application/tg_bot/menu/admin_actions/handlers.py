from datetime import datetime, timedelta

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from loguru import logger
from aiogram.utils.link import create_telegram_link

from application.tg_bot.filters.is_admin import is_super_admin
from application.tg_bot.menu.admin_actions.keyboards.menu_keyboard import get_admin_main_menu_keyboard, \
    back_to_admin_menu_keyboard
from utils.config import settings
from utils.deep_link import encode_date_token

router = Router()


@router.callback_query(F.data == "admin_main_menu_button")
async def start_admin_handler(callback_query: types.CallbackQuery, state: FSMContext):
    await state.clear()
    tg_id = callback_query.from_user.id
    logger.info(f"start_admin_handler is handled. TG id: {tg_id}")
    await callback_query.message.delete()
    await callback_query.message.answer("Привет! Вы в админ панели, что хотите изменить?",
                                        reply_markup=get_admin_main_menu_keyboard(
                                            is_super_admin(tg_id)))


@router.callback_query(F.data == "back_to_admin_main_menu")
async def back_admin_handler(callback_query: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback_query.message.delete()
    print(f'td_id - {callback_query.from_user.id}')
    await callback_query.message.answer("Вы вернулись в главное меню!",
                                        reply_markup=get_admin_main_menu_keyboard(
                                            is_super_admin(callback_query.from_user.id)))

@router.callback_query(F.data == "generate_deep_link")
async def generate_deep_link(callback_query: types.CallbackQuery):
    try:
        expire_date = datetime.now().replace(hour=23, minute=59, second=59) + timedelta(days=3)
        token = encode_date_token(expire_date)

        bot_username = settings.BOT_USERNAME
        if not bot_username:
            raise ValueError("settings.BOT_USERNAME не задан")

        link = create_telegram_link(bot_username, start=f"{token}")

        await callback_query.message.edit_text(
            f"🔗 Ваша пригласительная ссылка (действует до {expire_date.date()}):\n\n{link}",
            reply_markup=back_to_admin_menu_keyboard()
        )
        await callback_query.answer()

    except Exception:
        logger.exception("Ошибка при генерации ссылки")
        await callback_query.message.answer("⚠️ Ошибка при генерации ссылки. Обратитесь к администратору.")
