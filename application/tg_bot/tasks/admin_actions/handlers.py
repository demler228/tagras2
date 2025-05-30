from datetime import datetime
from loguru import logger
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram import Router, F, types
from domain.tasks.db_bl import TasksDbBl
from utils.data_state import DataSuccess
from utils.logs import admin_logger
from .edit_handler import handle_edit_task
from .reassign_task_handlers import handle_reassign_task
from .keyboards import (
    task_admin_panel_keyboard,
    task_action_keyboard,
    back_to_tasks_list,
    menu_of_action_after_creating,
    build_user_selection_keyboard,
    task_list_actions,
    back_to_task_actions
)
from .keyboards.callback_factories import (TaskActionCallbackFactory,
                                           UserIdCallbackFactory,
                                           PaginationCallbackFactory,
                                           BackTasksListAdminCallbackFactory,
                                           BackToActionsAdminCallbackFactory,
                                           PaginationTaskListCallbackFactory)

router = Router()

MAX_TEXT_LENGTH = 1000
# Состояния для просмотра задач
class ViewTaskStates(StatesGroup):
    select_task = State()


class CreateTaskStates(StatesGroup):
    name = State()
    description = State()
    deadline = State()


class AssignTaskStates(StatesGroup):
    select_users = State()

class TaskListPaginationStates(StatesGroup):
    viewing_page = State()


# Обработчик перехода в раздел задач
@router.callback_query(BackToActionsAdminCallbackFactory.filter())
@router.callback_query(F.data == "tasks_button_admin")
async def handle_tasks_button(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(
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
    try:

        deadline = message.text
        parsed_date = datetime.strptime(deadline, "%Y-%m-%d").date()
        current_date = datetime.today().date()

        if parsed_date < current_date:
            await message.answer(
                "Дедлайн не может быть раньше даты создания. Введите дедлайн заново (формат YYYY-MM-DD):")
            return
        else:
            data = await state.get_data()
            data_state = TasksDbBl.create_task(
                name=data['name'],
                description=data['description'],
                deadline=deadline
            )
            if isinstance(data_state, DataSuccess):
                task_id = data_state.data
                admin_logger.info(
                    f'админ {message.chat.full_name} создал задачу {data['name']}')
                await state.update_data(task_id=task_id)  # Сохраняем ID задачи в состоянии
                await message.answer(
                    f"Задача успешно создана! ID: {task_id}",
                    reply_markup=menu_of_action_after_creating()
                )
            else:
                await message.answer(f"Ошибка: {data_state.error_message}")

    except ValueError:
        await message.answer("Неверный формат даты. Введите дедлайн заново (формат YYYY-MM-DD):")


@router.callback_query(AssignTaskStates.select_users, UserIdCallbackFactory.filter())
async def select_user_handler(
        callback_query: types.CallbackQuery,
        state: FSMContext,
        callback_data: UserIdCallbackFactory
):
    try:
        await callback_query.answer()
        data = await state.get_data()
        user_id = callback_data.user_id
        task_id = callback_data.task_id
        current_page = data.get("current_page", 1)

        selected_users = set(data.get("selected_users", []))

        if user_id in selected_users:
            selected_users.remove(user_id)
        else:
            selected_users.add(user_id)

        await state.update_data(selected_users=list(selected_users), current_page=current_page)

        users_data_state = TasksDbBl.get_all_users()
        if not isinstance(users_data_state, DataSuccess) or not users_data_state.data:
            await callback_query.answer("Ошибка получения списка пользователей", show_alert=True)
            return

        updated_data = await state.get_data()
        logger.info(f"Содержимое state: {updated_data}")
        keyboard = build_user_selection_keyboard(users_data_state.data,
                                                 list(selected_users),
                                                 page=current_page,
                                                 task_id=task_id)
        await callback_query.message.edit_reply_markup(reply_markup=keyboard)

    except Exception as e:
        print(f"Ошибка в select_user_handler: {e}")
        await callback_query.answer("Произошла ошибка", show_alert=True)


@router.callback_query(PaginationCallbackFactory.filter())
async def pagination_handler(
        callback_query: types.CallbackQuery,
        callback_data: PaginationCallbackFactory,
        state: FSMContext
):
    try:
        await callback_query.answer()

        # Получаем данные из состояния
        data = await state.get_data()
        task_id = data.get("task_id")
        all_users_data_state = TasksDbBl.get_all_users()

        if isinstance(all_users_data_state, DataSuccess) and all_users_data_state.data:
            all_users = all_users_data_state.data
            selected_users = set(data.get("selected_users", []))

            # Обновляем текущую страницу на основе действия (prev/next)
            current_page = data.get("current_page", 1)
            if callback_data.action == "prev":
                current_page -= 1
            elif callback_data.action == "next":
                current_page += 1

            # Убедимся, что страница не выходит за границы
            total_pages = (len(all_users) + 9) // 10  # users_per_page = 10
            current_page = max(1, min(total_pages, current_page))

            # Сохраняем новую текущую страницу в состоянии
            await state.update_data(current_page=current_page)

            # Обновляем клавиатуру для новой страницы
            keyboard = build_user_selection_keyboard(
                all_users=all_users,
                selected_users=list(selected_users),
                page=current_page,
                users_per_page=10,
                task_id=task_id
            )
            await callback_query.message.edit_reply_markup(reply_markup=keyboard)
    except Exception as e:
        print(f"Ошибка в pagination_handler: {e}")
        await callback_query.answer("Произошла ошибка", show_alert=True)


@router.callback_query(AssignTaskStates.select_users, F.data == "done")
async def done_selecting_users(callback_query: types.CallbackQuery, state: FSMContext):
    try:
        data = await state.get_data()
        selected_users = data.get("selected_users", [])
        task_id = data.get("task_id")

        if not selected_users:
            await callback_query.answer("Выберите хотя бы одного пользователя!", show_alert=True)
            return
        # Назначаем задачу пользователям
        result = TasksDbBl.assign_task_to_user(task_id, selected_users)

        if isinstance(result, DataSuccess):
            await callback_query.message.edit_text("Пользователи успешно назначены на задачу!",
                                                   reply_markup=task_admin_panel_keyboard())
        else:
            await callback_query.message.edit_text(f"Ошибка: {result.error_message}")

        await state.clear()
    except Exception as e:
        print(f"Ошибка в done_selecting_users: {e}")
        await callback_query.answer("Произошла ошибка", show_alert=True)


def split_message_by_pages(message: str, max_length: int) -> list:
    pages = []
    current_page = ""

    # Разделяем сообщение на строки
    lines = message.split("\n")

    for line in lines:
        # Проверяем, влезет ли новая строка на текущую страницу
        if len(current_page) + len(line) + 1 <= max_length:  # +1 для символа "\n"
            current_page += line + "\n"
        else:
            # Если нет места, сохраняем текущую страницу и начинаем новую
            pages.append(current_page.strip())
            current_page = line + "\n"

    # Добавляем последнюю страницу, если она не пустая
    if current_page.strip():
        pages.append(current_page.strip())

    return pages

@router.callback_query(BackTasksListAdminCallbackFactory.filter())
@router.callback_query(F.data == "view_tasks")
async def view_tasks_handler(callback_query: types.CallbackQuery, state: FSMContext):
    data_state = TasksDbBl.get_all_tasks()
    logger.info("view_tasks_handler is handled")
    message = f"Список задач:\n\n"
    if isinstance(data_state, DataSuccess) and data_state.data:
        tasks = data_state.data

        for idx, task in enumerate(tasks, start=1):
            message += f"{idx}. {task.name}\n"

        # Разбиваем сообщение на страницы с учетом целостности строк
        pages = split_message_by_pages(message, MAX_TEXT_LENGTH)

        # Store the pages and current page in the state
        await state.set_state(TaskListPaginationStates.viewing_page)
        await state.update_data(pages=pages, current_page=1)
        await state.set_state(ViewTaskStates.select_task)

        await callback_query.message.edit_text(
            pages[0] + "\n\nВведите номер задачи для просмотра деталей:",
            reply_markup=task_list_actions(1, len(pages))
        )
    else:
        await callback_query.message.answer("Задачи не найдены", reply_markup=back_to_task_actions())

@router.callback_query(PaginationTaskListCallbackFactory.filter())
async def task_list_pagination_handler(callback_query: types.CallbackQuery, state: FSMContext, callback_data: PaginationTaskListCallbackFactory ):
    logger.info("task_list_pagination_handler is handled")
    data = await state.get_data()
    pages = data['pages']
    current_page = data['current_page']

    action = callback_data.action
    page = callback_data.page
    page = int(page)

    if action == "next_page" and page <= len(pages):
        current_page = page
        logger.info("next button is handled")
    elif action == "prev_page" and page >= 1:
        current_page = page
        logger.info("previous button is handled")

    await state.update_data(current_page=current_page)

    await callback_query.message.edit_text(
        pages[current_page -1] + "\n\nВведите номер задачи для просмотра деталей:",
        reply_markup=task_list_actions(current_page, len(pages))
    )
    await state.set_state(ViewTaskStates.select_task)
    await callback_query.answer()


@router.message(ViewTaskStates.select_task)
async def select_task_handler(message: types.Message, state: FSMContext):
    try:
        logger.info(f"select_task_handler is handled")
        task_number = int(message.text) - 1
        data_state = TasksDbBl.get_all_tasks()
        logger.info(f"Task number: {task_number}")

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
                await message.answer("Некорректный номер задачи. Попробуйте снова.", reply_markup=back_to_tasks_list())
        else:
            await message.answer("Задачи не найдены", reply_markup=back_to_tasks_list())
    except ValueError:
        await message.answer("Введите корректный номер задачи.", reply_markup=back_to_tasks_list())
    finally:
        await state.clear()


@router.callback_query(TaskActionCallbackFactory.filter())
async def task_action_handler(
        callback_query: types.CallbackQuery,
        callback_data: TaskActionCallbackFactory,
        state: FSMContext
):
    task_id = callback_data.task_id
    action = callback_data.action
    await state.update_data(task_id=task_id)
    if action == "delete_task":
        TasksDbBl.delete_task(task_id) # проверки нету !!!!! если будут проблемы с бд, то должны выкинуть пользователю сообщение об ошибке
        admin_logger.info(
            f'админ {callback_query.message.chat.full_name} удалил задачу {task_id} id')
        await callback_query.message.edit_text(f"Задача {task_id} удалена", reply_markup=back_to_tasks_list())
    elif action == "edit_task":
        await handle_edit_task(callback_query, task_id)
    elif action == "reassign_task":
        await handle_reassign_task(callback_query, state)


@router.callback_query(F.data == "assign_task")
async def handle_assign_task(callback_query: types.CallbackQuery, state: FSMContext):
    try:
        data = await state.get_data()
        task_id = data.get("task_id")

        if not task_id:
            await callback_query.message.answer("Ошибка: ID задачи не найден.")
            return

        users_data_state = TasksDbBl.get_all_users()

        if isinstance(users_data_state, DataSuccess) and users_data_state.data:
            all_users = users_data_state.data
            if not all_users:
                await callback_query.message.answer("Список пользователей пуст.")
                return

            keyboard = build_user_selection_keyboard(all_users, task_id=task_id)

            msg = await callback_query.message.edit_text(
                "Выберите пользователей для назначения задачи:",
                reply_markup=keyboard
            )

            await state.update_data(
                task_id=task_id,
                selected_users=[],
                message_with_users=msg.message_id
            )
            await state.set_state(AssignTaskStates.select_users)
        else:
            await callback_query.message.answer("Ошибка при получении списка пользователей.")
    except Exception as e:
        logger.error(f"Ошибка в handle_assign_task: {e}")
        await callback_query.message.answer("Произошла ошибка при обработке запроса.")

