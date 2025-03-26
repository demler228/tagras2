from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram import Router, F, types
from domain.tasks.db_bl import TasksDbBl
from utils.data_state import DataSuccess
from .keyboards import (
    task_admin_panel_keyboard,
    task_action_keyboard,
    back_to_tasks_list,
    get_all_tasks_button, menu_of_action_after_creating
)
from .keyboards.callback_factories import TaskActionCallbackFactory

router = Router()

# Состояния для просмотра задач
class ViewTaskStates(StatesGroup):
    select_task = State()

class CreateTaskStates(StatesGroup):
    name = State()
    description = State()
    deadline = State()

# Обработчик перехода в раздел задач
@router.callback_query(F.data == "tasks_button_admin")
async def handle_tasks_button(callback_query: types.CallbackQuery):
    await callback_query.message.answer(
        "Вы в разделе задач:",
        reply_markup=task_admin_panel_keyboard()
    )

# Обработчик создания новой задачи
@router.callback_query(F.data == "create_task")
async def start_create_task(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.answer("Введите название задачи:")
    await state.set_state(CreateTaskStates.name)

@router.message(CreateTaskStates.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введите описание задачи:")
    await state.set_state(CreateTaskStates.description)

@router.message(CreateTaskStates.description)
async def process_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer("Введите дедлайн задачи (формат YYYY-MM-DD):")
    await state.set_state(CreateTaskStates.deadline)

@router.message(CreateTaskStates.deadline)
async def process_deadline(message: types.Message, state: FSMContext):
    deadline = message.text
    data = await state.get_data()

    data_state = TasksDbBl.create_task(
        name=data['name'],
        description=data['description'],
        deadline=deadline
    )

    if isinstance(data_state, DataSuccess):
        await message.answer(f"Задача успешно создана! ID: {data_state.data}", reply_markup=menu_of_action_after_creating())
    else:
        await message.answer(f"Ошибка: {data_state.error_message}")

    await state.clear()

# Обработчик просмотра задач
@router.callback_query(F.data == "view_tasks")
async def view_tasks_handler(callback_query: types.CallbackQuery, state: FSMContext):
    data_state = TasksDbBl.get_all_tasks()

    if isinstance(data_state, DataSuccess) and data_state.data:
        tasks = data_state.data
        message = "Список задач:\n\n"

        for idx, task in enumerate(tasks, start=1):
            message += f"{idx}. {task.name}\n"

        await callback_query.message.answer(
            message + "\nВведите номер задачи для просмотра деталей:",
            reply_markup=back_to_tasks_list()
        )
        await state.set_state(ViewTaskStates.select_task)
    else:
        await callback_query.message.answer("Задачи не найдены", reply_markup=back_to_tasks_list())

# Обработчик выбора задачи по номеру
@router.message(ViewTaskStates.select_task)
async def select_task_handler(message: types.Message, state: FSMContext):
    try:
        task_number = int(message.text) - 1  # Номер начинается с 1
        data_state = TasksDbBl.get_all_tasks()

        if isinstance(data_state, DataSuccess) and data_state.data:
            tasks = data_state.data

            if 0 <= task_number < len(tasks):
                task = tasks[task_number]

                # Формируем сообщение с информацией о задаче
                text = (
                    f"<b>Задача:</b> {task.name}\n\n"
                    f"<b>Описание:</b> {task.description if task.description else 'Нет описания'}\n\n"
                    f"<b>Дата создания:</b> {task.creation_date.strftime('%Y-%m-%d')}\n\n"
                    f"<b>Дедлайн:</b> {task.deadline.strftime('%Y-%m-%d') if task.deadline else 'Не указан'}"
                )

                await message.answer(
                    text,
                    parse_mode="HTML",
                    reply_markup=task_action_keyboard(task.id)
                )
            else:
                await message.answer("Некорректный номер задачи. Попробуйте снова.")
        else:
            await message.answer("Задачи не найдены")
    except ValueError:
        await message.answer("Введите корректный номер задачи.")
    finally:
        await state.clear()

# Обработчик действий с задачей
@router.callback_query(TaskActionCallbackFactory.filter())
async def task_action_handler(
    callback_query: types.CallbackQuery,
    callback_data: TaskActionCallbackFactory
):
    task_id = callback_data.task_id
    action = callback_data.action

    if action == "edit":
        await callback_query.message.answer(f"Редактирование задачи {task_id}...")
    elif action == "reassign":
        await callback_query.message.answer(f"Переопределение исполнителей для задачи {task_id}...")
    elif action == "delete":
        await callback_query.message.answer(f"Удаление задачи {task_id}...", reply_markup=back_to_tasks_list())



