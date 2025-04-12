from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from .callback_factories import (
    TaskAdminCallbackFactory,
    BackTasksListAdminCallbackFactory,
    BackToMenuAdminCallbackFactory,
    TaskActionCallbackFactory,
    UserIdCallbackFactory,
    PaginationCallbackFactory,
    UpdateActionCallbackFactory,
    BackToActionsAdminCallbackFactory,
    PaginationTaskListCallbackFactory
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
        text="Редактировать задачу",
        callback_data=TaskActionCallbackFactory(action="edit_task", task_id=task_id)
    )
    builder.button(
        text="Переопределить исполнителей",
        callback_data=TaskActionCallbackFactory(action="reassign_task", task_id=task_id)
    )
    builder.button(
        text="Удалить задачу",
        callback_data=TaskActionCallbackFactory(action="delete_task", task_id=task_id)
    )
    builder.button(
        text="🔙 Назад к списку заданий",
        callback_data=BackTasksListAdminCallbackFactory()
    )
    builder.adjust(1)
    return builder.as_markup()


def update_task_actions(task_id):
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Изменить название",
        callback_data=UpdateActionCallbackFactory(action="update_name", task_id=task_id).pack()
    )
    builder.button(
        text="Изменить описание",
        callback_data=UpdateActionCallbackFactory(action="update_description", task_id=task_id).pack()
    )
    builder.button(
        text="Изменить дедлайн",
        callback_data=UpdateActionCallbackFactory(action="update_deadline", task_id=task_id).pack()
    )
    builder.button(text="🔙 Назад к действиям",
                   callback_data=UpdateActionCallbackFactory(action="back_to_task_actions", task_id=task_id))
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


def task_list_actions(current_page: int, total_pages: int):

    builder = InlineKeyboardBuilder()
    if current_page > 1:
        builder.button(
            text="⬅️",
            callback_data=PaginationTaskListCallbackFactory(action="prev_page", page=current_page - 1).pack()
        )


    if current_page < total_pages:
        builder.button(
            text="➡️",
            callback_data=PaginationTaskListCallbackFactory(action="next_page", page=current_page + 1).pack()
        )

    builder.button(
        text="🔙 Назад к действиям",
        callback_data=BackToActionsAdminCallbackFactory()
    )
    builder.adjust(2, 1)
    return builder.as_markup()



def back_to_task_actions():

    builder = InlineKeyboardBuilder()
    builder.button(
        text="🔙 Назад к действиям",
        callback_data=BackToActionsAdminCallbackFactory()
    )
    builder.adjust(1)
    return builder.as_markup()

def build_user_selection_keyboard(
        all_users: list,
        selected_users: list = None,
        page: int = 1,
        users_per_page: int = 10,
        task_id: int = None,
):
    if selected_users is None:
        selected_users = []

    # Вычисляем индексы для текущей страницы
    start_index = (page - 1) * users_per_page
    end_index = start_index + users_per_page
    paginated_users = all_users[start_index:end_index]

    builder = InlineKeyboardBuilder()

    # Добавляем пользователей для текущей страницы
    for user in paginated_users:
        user_label = f"{user.username} ✅" if user.id in selected_users else user.username
        callback_data = UserIdCallbackFactory(user_id=user.id, task_id=task_id).pack()
        builder.button(text=user_label, callback_data=callback_data)

    # Добавляем кнопки пагинации
    total_pages = (len(all_users) + users_per_page - 1) // users_per_page  # Вычисляем общее количество страниц
    if total_pages > 1:
        buttons = []
        if page > 1:
            buttons.append(InlineKeyboardButton(
                text="⬅️ Предыдущая страница",
                callback_data=PaginationCallbackFactory(action="prev", page=page - 1, task_id=task_id).pack()
            ))
        if page < total_pages:
            buttons.append(InlineKeyboardButton(
                text="➡️ Следующая страница",
                callback_data=PaginationCallbackFactory(action="next", page=page + 1, task_id=task_id).pack()
            ))
        builder.row(*buttons)

    # Добавляем кнопку "Готово"
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


def skip_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="Отмена", callback_data="skip")
    builder.adjust(1)
    return builder.as_markup()
