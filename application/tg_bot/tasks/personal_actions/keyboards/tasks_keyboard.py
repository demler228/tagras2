from aiogram.utils.keyboard import InlineKeyboardBuilder
from application.tg_bot.office_maps.personal_actions.keyboards.callback_factories import BackToSectionCallbackFactory
from domain.tasks.db_bl import TasksDbBl

from .callback_factories import (
    TaskPersonalCallbackFactory, BackTasksListCallbackFactory
)
from application.tg_bot.faq.personal_actions.keyboards import BackToMenuCallbackFactory
from utils.data_state import DataSuccess


def get_tasks_for_user_keyboard(tg_id):
    builder = InlineKeyboardBuilder()

    # Получаем список зданий из базы данных
    data_state = TasksDbBl.get_tasks_by_tg_id(tg_id)
    if isinstance(data_state, DataSuccess):
        for task in data_state.data:
            builder.button(
                text=task.name,
                callback_data=TaskPersonalCallbackFactory(task_id=task.id)
            )
    else:
        # Если данные не получены, можно добавить кнопку с сообщением об ошибке
        builder.button(text="Ошибка загрузки заданий", callback_data="error")

    builder.button(
        text="🔙 Назад в меню",
        callback_data=BackToMenuCallbackFactory()
    )
    builder.adjust(1)
    return builder.as_markup()


def back_to_tasks_list_personal():
    builder = InlineKeyboardBuilder()

    builder.button(text="🔙 Назад к списку заданий", callback_data=BackTasksListCallbackFactory())

    builder.adjust(1)
    return builder.as_markup()
