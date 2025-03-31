from datetime import datetime
from loguru import logger
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram import Router, F, types
from domain.tasks.db_bl import TasksDbBl
from utils.data_state import DataSuccess

from .keyboards import (

    skip_keyboard,
    update_task_actions, task_action_keyboard,
)
from .keyboards.callback_factories import TaskActionCallbackFactory, UpdateActionCallbackFactory

router = Router()


class EditTaskStates(StatesGroup):
    task_id = State()
    edit_name = State()
    edit_description = State()
    edit_deadline = State()

@router.callback_query(F.data == "edit_task")
async def handle_edit_task(callback_query: types.CallbackQuery, task_id: int):
    try:
        logger.info(f"Id of task: {task_id}")

        await callback_query.message.edit_reply_markup(reply_markup=update_task_actions(task_id))
        print("Callback data:", callback_query.data)
    except Exception as e:
        logger.error(f"Ошибка в handle_edit_task: {e}")
        await callback_query.message.answer("Произошла ошибка при обработке запроса.")


@router.callback_query(UpdateActionCallbackFactory.filter(F.action == "update_name"))
async def start_edit_name(callback_query: types.CallbackQuery, callback_data: UpdateActionCallbackFactory,
                          state: FSMContext):
    logger.info("Edit_name handled")
    await state.set_state()
    print(f"Callback data: action={callback_data.action}, task_id={callback_data.task_id}")
    task_id = callback_data.task_id
    await state.update_data(task_id=task_id)
    await callback_query.message.answer(
        "Введите новое название задачи или нажмите 'Отмена':",
        reply_markup=skip_keyboard()
    )
    await state.set_state(EditTaskStates.edit_name)


@router.message(EditTaskStates.edit_name)
async def process_edit_name(message: types.Message,  state: FSMContext):
    if message.text.lower() == "пропустить":
        await message.answer("Редактирование названия пропущено.")
        await state.clear()
        return

    new_name = message.text
    data = await state.get_data()
    task_id = data['task_id']
    result = TasksDbBl.update_task(task_id, name=new_name)
    if isinstance(result, DataSuccess):
        tasks_data_state = TasksDbBl.get_all_tasks()
        tasks = tasks_data_state.data
        task = next((t for t in tasks if t.id == task_id), None)
        logger.info(f"task detail: {task.name}")
        text = (
            f"<b>Задача:</b> {task.name}\n\n"
            f"<b>Описание:</b> {task.description if task.description else 'Нет описания'}\n\n"
            f"<b>Дата создания:</b> {task.creation_date.strftime('%Y-%m-%d')}\n\n"
            f"<b>Дедлайн:</b> {task.deadline.strftime('%Y-%m-%d') if task.deadline else 'Не указан'}"
        )
        await message.answer(text, parse_mode="HTML", reply_markup=update_task_actions(task_id))
    else:
        await message.answer(f"Ошибка: {result.error_message}")



@router.callback_query(UpdateActionCallbackFactory.filter(F.action == "update_description"))
async def start_edit_description(callback_query: types.CallbackQuery, callback_data: UpdateActionCallbackFactory,
                                 state: FSMContext):
    task_id = callback_data.task_id
    await state.update_data(task_id=task_id)
    await callback_query.message.answer(
        "Введите новое описание задачи или нажмите 'Пропустить':",
        reply_markup=skip_keyboard()
    )
    await state.set_state(EditTaskStates.edit_description)


@router.message(EditTaskStates.edit_description)
async def process_edit_description(message: types.Message, state: FSMContext):
    if message.text.lower() == "пропустить":
        await message.answer("Редактирование описания пропущено.")
        await state.clear()
        return

    new_description = message.text
    data = await state.get_data()
    task_id = data['task_id']
    result = TasksDbBl.update_task(task_id, description=new_description)
    if isinstance(result, DataSuccess):
        tasks_data_state = TasksDbBl.get_all_tasks()
        tasks = tasks_data_state.data
        task = next((t for t in tasks if t.id == task_id), None)
        logger.info(f"task detail: {task.name}")
        text = (
            f"<b>Задача:</b> {task.name}\n\n"
            f"<b>Описание:</b> {task.description if task.description else 'Нет описания'}\n\n"
            f"<b>Дата создания:</b> {task.creation_date.strftime('%Y-%m-%d')}\n\n"
            f"<b>Дедлайн:</b> {task.deadline.strftime('%Y-%m-%d') if task.deadline else 'Не указан'}"
        )
        await message.answer(text, parse_mode="HTML", reply_markup=update_task_actions(task_id))
    else:
        await message.answer(f"Ошибка: {result.error_message}")
    await state.clear()


@router.callback_query(UpdateActionCallbackFactory.filter(F.action == "update_deadline"))
async def start_edit_deadline(callback_query: types.CallbackQuery, callback_data: UpdateActionCallbackFactory,
                              state: FSMContext):
    task_id = callback_data.task_id
    await state.update_data(task_id=task_id)
    await callback_query.message.answer(
        "Введите новый дедлайн (формат YYYY-MM-DD) или нажмите 'Пропустить':",
        reply_markup=skip_keyboard()
    )
    await state.set_state(EditTaskStates.edit_deadline)


@router.message(EditTaskStates.edit_deadline)
async def process_edit_deadline(message: types.Message, state: FSMContext):
    if message.text.lower() == "пропустить":
        await message.answer("Редактирование дедлайна пропущено.")
        await state.clear()
        return

    try:
        new_deadline = message.text
        parsed_date = datetime.strptime(new_deadline, "%Y-%m-%d").date()
        current_date = datetime.today().date()
        if parsed_date < current_date:
            await message.answer("Дедлайн не может быть раньше даты создания. Введите дедлайн заново:")
            return
        data = await state.get_data()
        task_id = data['task_id']
        result = TasksDbBl.update_task(task_id, deadline=new_deadline)
        if isinstance(result, DataSuccess):
            tasks_data_state = TasksDbBl.get_all_tasks()
            tasks = tasks_data_state.data
            task = next((t for t in tasks if t.id == task_id), None)
            logger.info(f"task detail: {task.name}")
            text = (
                f"<b>Задача:</b> {task.name}\n\n"
                f"<b>Описание:</b> {task.description if task.description else 'Нет описания'}\n\n"
                f"<b>Дата создания:</b> {task.creation_date.strftime('%Y-%m-%d')}\n\n"
                f"<b>Дедлайн:</b> {task.deadline.strftime('%Y-%m-%d') if task.deadline else 'Не указан'}"
            )
            await message.answer(text, parse_mode="HTML", reply_markup=update_task_actions(task_id))
        else:
            await message.answer(f"Ошибка: {result.error_message}")
    except ValueError:
        await message.answer("Неверный формат даты. Введите дедлайн заново (формат YYYY-MM-DD):")
    finally:
        await state.clear()


@router.callback_query(F.data == "skip")
async def handle_skip(callback_query: types.CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state in [
        EditTaskStates.edit_name,
        EditTaskStates.edit_description,
        EditTaskStates.edit_deadline
    ]:
        await callback_query.answer("Редактирование пропущено.")
        await state.clear()
        await callback_query.message.answer("Редактирование параметра пропущено.")
    else:
        await callback_query.answer("Нечего пропускать.")

@router.callback_query(UpdateActionCallbackFactory.filter(F.action == "back_to_task_actions"))
async def handle_back_to_actions(callback_query: types.CallbackQuery, state: FSMContext,  callback_data: UpdateActionCallbackFactory):
    try:
        logger.info("back_to_task is handled")

        task_id = callback_data.task_id

        logger.info(f"task_id: {task_id}")


        if not task_id:
            await callback_query.answer("Ошибка: ID задачи не найден.", show_alert=True)
            return

        # Получаем данные задачи из базы данных
        tasks_data_state = TasksDbBl.get_all_tasks()
        if not isinstance(tasks_data_state, DataSuccess) or not tasks_data_state.data:
            await callback_query.answer("Ошибка: Задачи не найдены.", show_alert=True)
            return

        tasks = tasks_data_state.data
        task = next((t for t in tasks if t.id == task_id), None)

        if not task:
            await callback_query.answer("Ошибка: Задача не найдена.", show_alert=True)
            return

        # Формируем текст с деталями задачи
        text = (
            f"<b>Задача:</b> {task.name}\n\n"
            f"<b>Описание:</b> {task.description if task.description else 'Нет описания'}\n\n"
            f"<b>Дата создания:</b> {task.creation_date.strftime('%Y-%m-%d')}\n\n"
            f"<b>Дедлайн:</b> {task.deadline.strftime('%Y-%m-%d') if task.deadline else 'Не указан'}"
        )

        # Отправляем сообщение с текстом и клавиатурой
        await callback_query.message.edit_reply_markup(
            text,
            parse_mode="HTML",
            reply_markup=task_action_keyboard(task.id)
        )
        await callback_query.answer()  # Подтверждаем получение callback
    except Exception as e:
        logger.error(f"Ошибка в handle_back_to_actions: {e}")
        await callback_query.answer("Произошла ошибка при возврате к действиям.", show_alert=True)
