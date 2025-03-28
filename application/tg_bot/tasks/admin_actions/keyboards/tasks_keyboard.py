from aiogram.utils.keyboard import InlineKeyboardBuilder
from .callback_factories import (
    TaskAdminCallbackFactory,
    BackTasksListAdminCallbackFactory,
    BackToMenuAdminCallbackFactory,
    TaskActionCallbackFactory,
    UserIdCallbackFactory
)

from domain.tasks.db_bl import TasksDbBl
from utils.data_state import DataSuccess

def task_admin_panel_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="Создать новую задачу", callback_data="create_task")
    builder.button(text="Просмотреть задачи", callback_data="view_tasks")
    builder.button(text="🔙 Назад в меню", callback_data=BackToMenuAdminCallbackFactory())
    builder.adjust(1)
    return builder.as_markup()

def task_action_keyboard(task_id):
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Изменить задачу",
        callback_data=TaskActionCallbackFactory(action="edit", task_id=task_id)
    )
    builder.button(
        text="Переопределить исполнителей",
        callback_data=TaskActionCallbackFactory(action="reassign", task_id=task_id)
    )
    builder.button(
        text="Удалить задачу",
        callback_data=TaskActionCallbackFactory(action="delete", task_id=task_id)
    )
    builder.adjust(1)
    return builder.as_markup()

def back_to_tasks_list():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="🔙 Назад к списку заданий",
        callback_data=BackTasksListAdminCallbackFactory()
    )
    builder.adjust(1)
    return builder.as_markup()


def build_user_selection_keyboard(all_users: list, selected_users: list = None):
    if selected_users is None:
        selected_users = []

    builder = InlineKeyboardBuilder()
    for user in all_users:
        user_label = f"{user.username} ✅" if user.id in selected_users else user.username
        callback_data = UserIdCallbackFactory(user_id=user.id).pack()
        builder.button(text=user_label, callback_data=callback_data)

    builder.button(text="Готово", callback_data="done")
    builder.adjust(1)

    return builder.as_markup()

def menu_of_action_after_creating():
    builder = InlineKeyboardBuilder()
    builder.button(text="Присвоить задачу", callback_data="assign_task")
    builder.adjust(1)
    return builder.as_markup()



def get_all_tasks_button():
    builder = InlineKeyboardBuilder()

    # Получаем список зданий из базы данных
    data_state = TasksDbBl.get_all_tasks()
    if isinstance(data_state, DataSuccess):
        for task in data_state.data:
            builder.button(
                text=task.name,
                callback_data=TaskAdminCallbackFactory(task_id=task.id)
            )
    else:
        # Если данные не получены, можно добавить кнопку с сообщением об ошибке
        builder.button(text="Ошибка загрузки заданий", callback_data="error")

    builder.button(
        text="🔙 Назад к действиям",
        callback_data=BackToMenuAdminCallbackFactory()
    )
    builder.adjust(1)
    return builder.as_markup()


