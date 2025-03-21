from aiogram.utils.keyboard import InlineKeyboardBuilder
from application.tg_bot.office_maps.personal_actions.keyboards.callback_factories import BackToSectionCallbackFactory
from domain.tasks.db_bl import TasksDbBl

from .callback_factories import (
    TaskCallbackFactory
)
from application.tg_bot.faq.personal_actions.keyboards import BackToMenuCallbackFactory
from utils.data_state import DataSuccess


def get_tasks_keyboard():
    builder = InlineKeyboardBuilder()

    # Получаем список зданий из базы данных
    data_state = TasksDbBl.get_tasks()
    if isinstance(data_state, DataSuccess):
        for task in data_state.data:
            builder.button(
                text=task.name,
                callback_data=TaskCallbackFactory(task_id=task.id)
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
