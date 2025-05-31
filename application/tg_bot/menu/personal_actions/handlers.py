from datetime import datetime, timedelta

from aiogram import Router, types, F
from aiogram.filters import CommandStart, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove
from sympy import print_glsl

from application.tg_bot.filters.is_admin import is_admin
from application.tg_bot.menu.personal_actions.keyboards.menu_keyboard import get_main_menu_keyboard, get_phone_keyboard
from application.tg_bot.menu.personal_actions.states import RegistrationStates
from application.tg_bot.user.entities.user import User
from domain.user.bl_models.db_bl import UserBL
from utils.data_state import DataSuccess, DataFailedMessage
from utils.deep_link import decode_date_token


router = Router()

@router.message(CommandStart(deep_link=True))
async def start_handler_with_token(message: types.Message, command: CommandObject, state: FSMContext):
    telegram_id = message.from_user.id
    data_state = UserBL.get_user_by_telegram_id(telegram_id)

    if isinstance(data_state, DataSuccess):
        await message.answer(
            "Привет! Я бот для адаптации сотрудников. Выберите, чем я могу помочь!",
            reply_markup=get_main_menu_keyboard(is_admin(message.from_user.id))
        )
        return

    expire_date = decode_date_token(command.args)
    if not expire_date or expire_date < datetime.now():
        await message.answer("Ссылка недействительна или срок действия истёк.")
        return

    await state.update_data(
        telegram_id=telegram_id,
        tg_username=message.from_user.username,
    )

    await message.answer(
        "Привет, вижу, что вы перешли по пригласительной ссылке. Для начала, как вас зовут?"
    )
    await state.set_state(RegistrationStates.waiting_for_name)


@router.message(RegistrationStates.waiting_for_name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(username=message.text)
    await message.answer(
        "Отлично, теперь нужно отправить номер телефона. Для этого нажмите на кнопку ниже",
        reply_markup=get_phone_keyboard()
    )

    await state.set_state(RegistrationStates.waiting_for_phone)


@router.message(RegistrationStates.waiting_for_phone, F.contact)
async def process_phone(message: types.Message, state: FSMContext):
    if not message.contact:
        await message.answer("Пожалуйста, отправьте номер телефона с помощью кнопки ниже.")
        return

    data = await state.get_data()

    user_info = User(
        telegram_id=data.get("telegram_id"),
        tg_username=data.get("tg_username"),
        username=data.get("username"),
        phone=message.contact.phone_number
    )

    user_state = UserBL.add_employee(user_info)
    if isinstance(user_state, DataFailedMessage):
        await message.answer("Не удалось зарегистрироваться, повторите позже.",
                             reply_markup=ReplyKeyboardRemove())
        return

    user = user_state.data

    await message.answer(
        f"Отлично, {user.username}, вы зарегистрированы!",
        reply_markup=ReplyKeyboardRemove()
    )

    await message.answer(
        "Вот главное меню:",
        reply_markup=get_main_menu_keyboard(is_admin(message.from_user.id))
    )

    await state.clear()


@router.message(CommandStart())
async def start_handler(message: types.Message):
    telegram_id = message.from_user.id

    data_state = UserBL.get_user_by_telegram_id(telegram_id)
    if isinstance(data_state, DataSuccess):
        await message.answer(
            "Привет! Я бот для адаптации сотрудников. Выберите, чем я могу помочь!",
            reply_markup=get_main_menu_keyboard(is_admin(message.from_user.id))
        )
    else:
        await message.answer(
            "Этот бот рассчитан на сотрудников компании Таграс. "
            "Если вы им являетесь и читаете данное сообщение, то обратитесь к своему руководителю, чтобы вам выдали доступ к боту!"
        )


@router.callback_query(F.data == "back_to_main_menu")
async def back_handler(callback_query: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback_query.message.delete()
    await callback_query.message.answer(
        "Вы вернулись в главное меню!",
        reply_markup=get_main_menu_keyboard(is_admin(callback_query.from_user.id))
    )
