from random import randint

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from application.tg_bot.training.admin_actions.keyboards.theme_list_keyboard import ThemeListCallback, \
    get_theme_list_keyboard, ThemeCallback
from application.tg_bot.training.admin_actions.keyboards.theme_menu_keyboard import get_theme_menu_keyboard
from application.tg_bot.training.entities.theme import Theme
from domain.training.education.bl_models import EducationBL
from utils.data_state import DataSuccess

router = Router()


class AdminStates(StatesGroup):
    theme_menu = State()
    change_theme_name = State()
    create_theme_name = State()


emoji_books = ['📒', '📕', '📗', '📘', '📙']


async def get_theme(state, callback_query=None, callback_data=None, message=None):
    await state.set_state(AdminStates.theme_menu)
    if message is None:
        await callback_query.message.delete()
        theme_list = (await state.get_data())['theme_list']
        theme = next((theme for theme in theme_list if theme.id == callback_data.theme_id), None)

        data_state = EducationBL.get_materials(theme.id)

        if isinstance(data_state, DataSuccess):
            materials = data_state.data
            message = await callback_query.message.answer(
                f"{emoji_books[randint(0, len(emoji_books) - 1)]} <b>{theme.name}</b>\n\n {'\n'.join([f'{material.title}:\n{material.url}' for material in materials])}",
                reply_markup=get_theme_menu_keyboard(), parse_mode='HTML')
        else:
            await callback_query.message.answer(f'❌ {data_state.error_message}')

    else:
        # если вдруг еще кто-то изменяет этот вопрос-ответ, чтобы были актуальные данные
        data_state = EducationBL.get_themes()

        if isinstance(data_state, DataSuccess):
            theme_list = data_state.data
            changed_theme_id = (await state.get_data())['theme'].id
            theme = next((theme for theme in theme_list if theme.id == changed_theme_id), None)

            data_state = EducationBL.get_materials(theme.id)

            if isinstance(data_state, DataSuccess):
                materials = data_state.data
                message = await callback_query.message.answer(
                    f"{emoji_books[randint(0, len(emoji_books) - 1)]} <b>{theme.name}</b>\n\n {'\n'.join([f'{material.title}:\n{material.url}' for material in materials])}",
                    reply_markup=get_theme_menu_keyboard(), parse_mode='HTML')
            else:
                await callback_query.message.answer(f'❌ {data_state.error_message}')

        else:
            await callback_query.message.answer(f'❌ {data_state.error_message}')
            return
    #стараемся минимизировать кол-во обращений к бд
    await state.update_data({'theme': theme, 'message': message})


async def get_theme_list_button(callback_query: types.CallbackQuery, state: FSMContext,
                                callback_data: ThemeListCallback = None):
    await callback_query.message.delete()

    data_state = EducationBL.get_themes()
    if isinstance(data_state, DataSuccess):
        if 'page' in (await state.get_data()) and callback_data is None:
            page = (await state.get_data())['page']
        else:
            page = callback_data.page if callback_data is not None else 1

        await state.set_data({'theme_list': data_state.data, 'page': page})

        await callback_query.message.answer("📚 Выберите тему:",
                                            reply_markup=get_theme_list_keyboard(data_state.data, page))
    else:
        await callback_query.message.answer(f'❌ {data_state.error_message}')


@router.callback_query(F.data == "training_button_admin")
async def handle_theme_list_button(callback_query: types.CallbackQuery, state: FSMContext):
    await get_theme_list_button(callback_query, state)


@router.callback_query(ThemeListCallback.filter())
async def handle_theme_list_button_by_callback(callback_query: types.CallbackQuery, state: FSMContext,
                                               callback_data: ThemeListCallback):
    await get_theme_list_button(callback_query, state, callback_data)


@router.callback_query(ThemeCallback.filter())
async def handle_theme_button(callback_query: types.CallbackQuery, callback_data: ThemeCallback, state: FSMContext):
    await get_theme(state, callback_query=callback_query, callback_data=callback_data)


@router.callback_query(F.data == "theme_delete_button")
async def handle_theme_delete_button(callback_query: types.CallbackQuery, state: FSMContext):
    theme = (await state.get_data())['theme']
    data_state = EducationBL.theme_delete(theme)

    if isinstance(data_state, DataSuccess):
        #await (await state.get_data())['message'].delete()
        await get_theme_list_button(callback_query, state)
        await callback_query.message.answer(f'Тема удалена!')
    else:
        await callback_query.message.answer(f'❌ {data_state.error_message}')


@router.callback_query(F.data == "theme_create_button")
async def theme_create_name(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(AdminStates.create_theme_name)
    await callback_query.message.answer(f"✍️ Введите название темы")


@router.message(F.text, AdminStates.create_theme_name)
async def theme_create(message: Message, state: FSMContext):
    theme = Theme(name=message.text)
    data_state = EducationBL.theme_create(theme)
    if isinstance(data_state, DataSuccess):
        theme.id = data_state.data
        await state.update_data({'theme': theme})
        await get_theme(state=state, message=message)
    else:
        await message.answer(f'❌ {data_state.error_message}')


@router.callback_query(F.data == "theme_change_question_button")
async def theme_change_question(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(AdminStates.change_theme_name)
    await callback_query.message.answer(f"✍️ Введите новое название темы")


@router.message(F.text, AdminStates.change_theme_name)
async def theme_changed_question(message: Message, state: FSMContext):
    theme = (await state.get_data())['theme']
    theme.name = message.text
    data_state = EducationBL.theme_update(theme)

    if isinstance(data_state, DataSuccess):
        await (await state.get_data())['message'].delete()
        await get_theme(state, message=message)
    else:
        await message.answer(f'❌ {data_state.error_message}')

