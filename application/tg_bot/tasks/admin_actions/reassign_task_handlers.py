from datetime import datetime
from loguru import logger
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram import Router, F, types
from domain.tasks.db_bl import TasksDbBl
from utils.data_state import DataSuccess, DataFailedMessage

from .keyboards import (

    skip_keyboard,
    update_task_actions, task_action_keyboard, back_to_tasks_list, build_user_selection_keyboard
)
from .keyboards.callback_factories import TaskActionCallbackFactory, UpdateActionCallbackFactory, UserIdCallbackFactory, \
    PaginationCallbackFactory

router = Router()


@router.callback_query(F.data == "reassign_task")
async def handle_reassign_task(callback_query: types.CallbackQuery, state: FSMContext):
    try:
        logger.info(f"handle_reassign_task is handled")
        state_data = await state.get_data()
        task_id = state_data.get("task_id")

        # Получаем всех пользователей
        all_users_data_state = TasksDbBl.get_all_users()
        if not isinstance(all_users_data_state, DataSuccess) or not all_users_data_state.data:
            await callback_query.answer("Не удалось получить список всех пользователей", show_alert=True)
            return

        all_users = all_users_data_state.data

        # Получаем назначенных пользователей
        assigned_users_data_state = TasksDbBl.get_assigned_users_by_task_id(task_id)
        if not isinstance(assigned_users_data_state, DataSuccess) or not assigned_users_data_state.data:
            selected_users = []  # Пустой список, если нет назначенных пользователей
        else:
            assigned_users = assigned_users_data_state.data
            selected_users = [user.id for user in assigned_users]

        # Сохраняем выбранных пользователей в состоянии
        await state.update_data(selected_users=selected_users, task_id=task_id)

        # Отображаем клавиатуру
        await callback_query.message.edit_reply_markup(
            reply_markup=build_user_selection_keyboard(
                all_users=all_users,
                selected_users=selected_users,
                page=1,
                users_per_page=10,
                task_id=task_id
            )
        )
    except Exception as e:
        logger.error(f"Ошибка в handle_reassign_task: {e}")
        await callback_query.message.answer("Произошла ошибка при обработке запроса.")

@router.callback_query(UserIdCallbackFactory.filter())
async def handle_user_selection(
    callback_query: types.CallbackQuery,
    callback_data: UserIdCallbackFactory,
    state: FSMContext
):
    try:
        logger.info(f"handle_user_selection is handled")
        user_id = callback_data.user_id
        task_id = callback_data.task_id

        # Получаем текущее состояние выбранных пользователей
        state_data = await state.get_data()
        selected_users = set(state_data.get("selected_users", []))
        new_page = state_data.get("current_page", 1)

        # Меняем состояние пользователя
        if user_id in selected_users:
            selected_users.remove(user_id)
        else:
            selected_users.add(user_id)

        # Сохраняем обновленное состояние
        await state.update_data(selected_users=list(selected_users))

        # Обновляем клавиатуру
        all_users_data_state = TasksDbBl.get_all_users()
        if not isinstance(all_users_data_state, DataSuccess) or not all_users_data_state.data:
            await callback_query.answer("Не удалось получить список всех пользователей", show_alert=True)
            return

        all_users = all_users_data_state.data

        await callback_query.message.edit_reply_markup(
            reply_markup=build_user_selection_keyboard(
                all_users=all_users,
                selected_users=list(selected_users),
                page=new_page,
                task_id=task_id
            )
        )
        logger.info(f"Содержимое FSMState: {state_data}")
        await callback_query.answer()
    except Exception as e:
        logger.error(f"Ошибка в handle_user_selection: {e}")
        await callback_query.message.answer("Произошла ошибка при обработке запроса.")
@router.callback_query(PaginationCallbackFactory.filter())
async def handle_pagination(
    callback_query: types.CallbackQuery,
    callback_data: PaginationCallbackFactory,
    state: FSMContext
):
    try:
        action = callback_data.action
        page = callback_data.page
        task_id = callback_data.task_id

        # Получаем текущее состояние выбранных пользователей
        state_data = await state.get_data()
        selected_users = state_data.get("selected_users", [])

        # Обновляем страницу в зависимости от действия
        if action == "prev":
            new_page = max(1, page - 1)
        elif action == "next":
            new_page = page + 1
        else:
            await callback_query.answer("Неверное действие пагинации", show_alert=True)
            return

        # Обновляем клавиатуру
        all_users_data_state = TasksDbBl.get_all_users()
        if not isinstance(all_users_data_state, DataSuccess) or not all_users_data_state.data:
            await callback_query.answer("Не удалось получить список всех пользователей", show_alert=True)
            return

        all_users = all_users_data_state.data

        await callback_query.message.edit_reply_markup(
            reply_markup=build_user_selection_keyboard(
                all_users=all_users,
                selected_users=selected_users,
                page=new_page,
                task_id=task_id
            )
        )
        await state.update_data(current_page=new_page)

        await callback_query.answer()
    except Exception as e:
        logger.error(f"Ошибка в handle_pagination: {e}")
        await callback_query.message.answer("Произошла ошибка при обработке запроса.")

@router.callback_query(F.data == "done")
async def handle_done(callback_query: types.CallbackQuery, state: FSMContext):
    try:
        # Получаем текущее состояние выбранных пользователей
        state_data = await state.get_data()
        selected_users = state_data.get("selected_users", [])
        task_id = state_data.get("task_id")

        logger.info(f"Содержимое FSMState в andle done: {state_data}")

        if not task_id:
            await callback_query.answer("ID задачи не найден", show_alert=True)
            return

        assign_result = TasksDbBl.assign_task_to_user(task_id, selected_users)
        if isinstance(assign_result, DataFailedMessage):
            await callback_query.answer(assign_result.message, show_alert=True)
            return
        await callback_query.answer(text="Переопределение пользователей совершено успешно", show_alert=True)
        await callback_query.message.edit_reply_markup(reply_markup=task_action_keyboard(task_id))
    except Exception as e:
        logger.error(f"Ошибка в handle_done: {e}")
        await callback_query.message.answer("Произошла ошибка при сохранении данных.")