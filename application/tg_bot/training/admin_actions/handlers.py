from random import randint
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ContentType
from aiogram.client.session.middlewares.request_logging import logger
import os
from pathlib import Path

from application.tg_bot.training.admin_actions.keyboards.theme_list_keyboard import ThemeListCallback, \
    get_theme_list_keyboard, ThemeCallback
from application.tg_bot.training.admin_actions.keyboards.theme_material_menu_keyboard import \
    get_theme_material_menu_keyboard
from application.tg_bot.training.admin_actions.keyboards.theme_menu_keyboard import get_theme_menu_keyboard
from application.tg_bot.training.admin_actions.keyboards.theme_choose_materials_keyboard import \
    ThemeChooseMaterialsCallback, get_theme_choose_materials_keyboard
from application.tg_bot.training.entities.materials import Material
from application.tg_bot.training.entities.theme import Theme
from domain.training.education.db_bl import EducationBL
from utils.data_state import DataSuccess
from domain.quiz.db_dal import FileRepository, WebRepository, QuizRepository
from utils.config import settings
from utils.logs import program_logger

router = Router()

# Папка для временного хранения файлов
TEMP_DIR = Path("temp_files")
TEMP_DIR.mkdir(exist_ok=True)

class AdminStates(StatesGroup):
    theme_menu = State()
    change_theme_name = State()
    create_theme_name = State()
    create_material_name = State()
    create_material_url = State()
    change_material_name = State()
    change_material_url = State()

emoji_books = ['📒', '📕', '📗', '📘', '📙']

async def get_theme(state, object, keyboard_markup, callback_data=None):
    await state.set_state(AdminStates.theme_menu)
    message = None
    data_state = None
    theme = None
    material_id = None

    if isinstance(object, Message):  # Проверяем, от кого вызвана функция: callback или message
        message = object
        data_state = EducationBL.get_themes()

        if isinstance(data_state, DataSuccess):
            await message.delete()
            theme_list = data_state.data
            changed_theme_id = (await state.get_data())['theme'].id
            theme = next((theme for theme in theme_list if theme.id == changed_theme_id), None)
            data_state = EducationBL.get_materials(theme.id)

            if callback_data:  # Проверка material_id
                if isinstance(data_state, DataSuccess):
                    materials = data_state.data
                    material_id = callback_data.material_id
                    material = next((material for material in materials if material.id == material_id), None)
                    await state.update_data({'material': material})
                else:
                    await message.answer(f'❌ {data_state.error_message}')
        else:
            await message.answer(f'❌ {data_state.error_message}')
    else:
        message = object.message
        await message.delete()
        theme_list = (await state.get_data())['theme_list']
        theme = next((theme for theme in theme_list if theme.id == callback_data.theme_id), None)
        data_state = EducationBL.get_materials(theme.id)

    if isinstance(data_state, DataSuccess):
        materials = data_state.data
        materials_text = '🧐 Материалов нету' if len(materials) == 0 else \
            '\n'.join([f'<u><b>[{i}]{material.title}:\n{material.url}</b></u>'
                       if material_id and material.id == material_id
                       else f'[{i}]{material.title}:\n{material.url}'
                       for i, material in enumerate(materials)])
        message = await message.answer(
            f"{emoji_books[randint(0, len(emoji_books) - 1)]} <b>{theme.name}</b>\n\n {materials_text}",
            reply_markup=keyboard_markup, parse_mode='HTML')
    else:
        await message.answer(f'❌ {data_state.error_message}')

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

@router.callback_query(ThemeChooseMaterialsCallback.filter())
async def handle_theme_choose_materials_button(callback_query: types.CallbackQuery, callback_data: ThemeChooseMaterialsCallback, state: FSMContext):
    await get_theme(state, callback_query.message, get_theme_material_menu_keyboard(), callback_data=callback_data)

@router.callback_query(ThemeCallback.filter())
async def handle_theme_button(callback_query: types.CallbackQuery, callback_data: ThemeCallback, state: FSMContext):
    await get_theme(state, callback_query, get_theme_menu_keyboard(), callback_data=callback_data)

@router.callback_query(F.data == "back_theme_button")
async def handle_theme_button(callback_query: types.CallbackQuery, state: FSMContext):
    await get_theme(state, callback_query.message, get_theme_menu_keyboard())

@router.callback_query(F.data == "theme_delete_button")
async def handle_theme_delete_button(callback_query: types.CallbackQuery, state: FSMContext):
    theme = (await state.get_data())['theme']
    data_state = EducationBL.theme_delete(theme)

    if isinstance(data_state, DataSuccess):
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
        await get_theme(state, message, get_theme_menu_keyboard())
    else:
        await message.answer(f'❌ {data_state.error_message}')

@router.callback_query(F.data == "theme_change_name_button")
async def theme_change_name(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(AdminStates.change_theme_name)
    await callback_query.message.answer(f"✍️ Введите новое название темы")

@router.message(F.text, AdminStates.change_theme_name)
async def theme_changed_name(message: Message, state: FSMContext):
    theme = (await state.get_data())['theme']
    theme.name = message.text
    data_state = EducationBL.theme_update(theme)

    if isinstance(data_state, DataSuccess):
        await (await state.get_data())['message'].delete()
        await get_theme(state, message, get_theme_menu_keyboard())
    else:
        await message.answer(f'❌ {data_state.error_message}')

@router.callback_query(F.data == "back_theme_choose_materials")
async def handle_back_theme_choose_button(callback_query: types.CallbackQuery, state: FSMContext):
    theme_id = (await state.get_data())['theme'].id
    data_state = EducationBL.get_materials(theme_id)

    if isinstance(data_state, DataSuccess):
        await get_theme(state, callback_query.message, get_theme_choose_materials_keyboard(data_state.data))
    else:
        await callback_query.message.answer(f'❌ {data_state.error_message}')

@router.callback_query(F.data == "theme_change_materials_button")
async def handle_back_theme_button(callback_query: types.CallbackQuery, state: FSMContext):
    theme_id = (await state.get_data())['theme'].id
    data_state = EducationBL.get_materials(theme_id)

    if isinstance(data_state, DataSuccess):
        await get_theme(state, callback_query.message, get_theme_choose_materials_keyboard(data_state.data))
    else:
        await callback_query.message.answer(f'❌ {data_state.error_message}')

@router.callback_query(F.data == "theme_create_material_button")
async def theme_create_material_name(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(AdminStates.create_material_name)
    await callback_query.message.answer(f"✍️ Введите название материала")

@router.message(F.text, AdminStates.create_material_name)
async def faq_create_answer(message: Message, state: FSMContext):
    await state.update_data({'material_name': message.text})
    await state.set_state(AdminStates.create_material_url)
    await message.answer(f"✍️ Введите URL или загрузите файл (PDF, Word, видео)")


# Обновление theme_created_material_url
@router.message(F.text, AdminStates.create_material_url)
async def theme_created_material_url(message: Message, state: FSMContext):
    theme = (await state.get_data())['theme']
    material = Material(
        title=(await state.get_data())['material_name'],
        url=message.text,
        theme_id=theme.id
    )
    data_state = EducationBL.material_create(material)

    if isinstance(data_state, DataSuccess):
        await (await state.get_data())['message'].delete()
        await get_theme(
            state,
            message,
            get_theme_material_menu_keyboard(),
            ThemeChooseMaterialsCallback(material_id=data_state.data)
        )

        # Проверка и обработка URL
        if not material.url.startswith(('http://', 'https://')):
            await message.answer("❌ Неверный формат ссылки! Пожалуйста, отправьте корректную URL (начинающуюся с http:// или https://).")
            return

        try:
            # Обработка URL и получение текста
            text = WebRepository.process_url(material.url)
            program_logger.debug(f"Извлечённый текст из URL {material.url}: {text}")
            if not text:
                await message.answer("ℹ️ Не удалось извлечь текст из ссылки для создания викторины.")
                return

            # Проверка токена
            token = settings.SBER_AUTH
            if not token:
                await message.answer("❌ Не удалось получить токен для генерации викторины.")
                return

            quiz_data = QuizRepository.get_quiz_questions(text)
            if isinstance(quiz_data, DataSuccess):
                save_result = QuizRepository.save_quiz(quiz_data.data, theme.name)
                if isinstance(save_result, DataSuccess):
                    await message.answer("✅ Викторина успешно создана и сохранена!")
                else:
                    await message.answer(f"❌ Ошибка при сохранении викторины: {save_result.error_message}")
            else:
                await message.answer(f"❌ Ошибка при генерации викторины: {quiz_data.error_message}")
        except Exception as e:
            program_logger.error(f"Ошибка при обработке URL {material.url}: {str(e)}")
            await message.answer(f"❌ Произошла ошибка при обработке ссылки: {str(e)}")
    else:
        await message.answer(f"❌ Ошибка при создании материала: {data_state.error_message}")

# Обновление theme_created_material_file
@router.message(F.content_type.in_({ContentType.DOCUMENT, ContentType.VIDEO}), AdminStates.create_material_url)
async def theme_created_material_file(message: Message, state: FSMContext, bot):
    theme = (await state.get_data())['theme']
    material_name = (await state.get_data())['material_name']

    # Определяем тип файла и получаем его
    if message.document:
        file_id = message.document.file_id
        file_name = message.document.file_name
    elif message.video:
        file_id = message.video.file_id
        file_name = f"{message.video.file_id}.mp4"  # Присваиваем расширение для видео
    else:
        await message.answer("❌ Неверный тип файла! Поддерживаются PDF, Word и видео.")
        return

    # Скачиваем файл
    file_info = await bot.get_file(file_id)
    program_logger.debug(f"Информация о файле: {file_info}")
    file_path = TEMP_DIR / file_name
    program_logger.debug(f"Путь к файлу: {file_path}")
    await bot.download_file(file_info.file_path, file_path)

    # Создаем объект Material с путем к файлу
    material = Material(
        title=material_name,
        url=str(file_path),  # Сохраняем путь к файлу как URL
        theme_id=theme.id
    )
    data_state = EducationBL.material_create(material)

    if isinstance(data_state, DataSuccess):
        await (await state.get_data())['message'].delete()
        await get_theme(
            state,
            message,
            get_theme_material_menu_keyboard(),
            ThemeChooseMaterialsCallback(material_id=data_state.data)
        )

        # Обработка содержимого файла с помощью FileRepository
        text = FileRepository.process_file(str(file_path))
        program_logger.debug(f"Извлечённый текст из файла {file_path}: {text}")
        if text:
            token = settings.SBER_AUTH
            if token:
                quiz_data = QuizRepository.get_quiz_questions(text)
                if isinstance(quiz_data, DataSuccess):
                    save_result = QuizRepository.save_quiz(quiz_data.data, theme.name)
                    if not isinstance(save_result, DataSuccess):
                        await message.answer(f'❌ Ошибка при сохранении викторины: {save_result.error_message}')
                    else:
                        await message.answer("✅ Викторина успешно создана и сохранена!")
                else:
                    await message.answer(f'❌ Ошибка при генерации викторины: {quiz_data.error_message}')
            else:
                await message.answer('❌ Не удалось получить токен для генерации викторины')
        else:
            await message.answer('ℹ️ Не удалось извлечь текст из файла для викторины')
    else:
        await message.answer(f'❌ {data_state.error_message}')

@router.callback_query(F.data == "change_material_name_button")
async def change_material_name(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(AdminStates.change_material_name)
    await callback_query.message.answer(f"✍️ Введите новое название материала")

@router.message(F.text, AdminStates.change_material_name)
async def material_changed_name(message: Message, state: FSMContext):
    material = (await state.get_data())['material']
    material.title = message.text
    data_state = EducationBL.material_update(material)

    if isinstance(data_state, DataSuccess):
        await (await state.get_data())['message'].delete()
        await get_theme(state, message, get_theme_material_menu_keyboard(),
                        ThemeChooseMaterialsCallback(material_id=material.id))
    else:
        await message.answer(f'❌ {data_state.error_message}')

@router.callback_query(F.data == "change_material_url_button")
async def change_material_url(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(AdminStates.change_material_url)
    await callback_query.message.answer(f"✍️ Введите новый URL или загрузите файл (PDF, Word, видео)")

@router.message(F.text, AdminStates.change_material_url)
async def changed_material_url(message: Message, state: FSMContext):
    material = (await state.get_data())['material']
    material.url = message.text
    data_state = EducationBL.material_update(material)

    if isinstance(data_state, DataSuccess):
        await (await state.get_data())['message'].delete()
        await get_theme(state, message, get_theme_material_menu_keyboard(),
                        ThemeChooseMaterialsCallback(material_id=material.id))
    else:
        await message.answer(f'❌ {data_state.error_message}')

@router.callback_query(F.data == "material_delete_button")
async def change_material_url(callback_query: types.CallbackQuery, state: FSMContext):
    material = (await state.get_data())['material']
    data_state = EducationBL.material_delete(material)

    if isinstance(data_state, DataSuccess):
        await get_theme(state, callback_query.message, get_theme_menu_keyboard())
        await callback_query.message.answer(f"Материал удален!")
    else:
        await callback_query.message.answer(f'❌ {data_state.error_message}')