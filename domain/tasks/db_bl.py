# db_bl.py
import os

from loguru import logger

from application.tg_bot.tasks.entities.task import Task
from application.tg_bot.tasks.entities.user_tasks import UserTask
from .db_dal import TasksDbDal
from utils.data_state import DataSuccess, DataState
from ..user.dal_models.db_dal import UserDbDal


class TasksDbBl:

    @staticmethod
    def get_tasks_by_tg_id(tg_id) -> DataState[list[Task]]:
        data_state = UserDbDal.get_user_by_telegram_id(tg_id)
        if isinstance(data_state, DataSuccess):
            user_id = data_state.data.id
            data_state = TasksDbDal.get_tasks_by_user_id(user_id)
        return data_state

    @staticmethod
    def get_all_tasks() -> DataState[list[Task]]:
        data_state = TasksDbDal.get_all_tasks()
        return data_state
    @staticmethod
    def create_task(name: str, description: str, deadline: str = None) -> DataState:
        return TasksDbDal.create_task(name, description, deadline)
    @staticmethod
    def get_task_by_task_id(task_id: int) -> DataState:
        return TasksDbDal.get_task_by_task_id(task_id)

    # @staticmethod
    # def assign_task_to_user(task_id: int, user_tg_id: int) -> DataState:
    #     data_state = UserDbDal.get_user_by_telegram_id(user_tg_id)
    #     if isinstance(data_state, DataSuccess):
    #         user_id = data_state.data.id
    #         return TasksDbDal.assign_task_to_user(task_id, user_id)
    #     return DataFailedMessage('Пользователь не найден!')

    @staticmethod
    def update_task(task_id: int, name: str = None, description: str = None, deadline: str = None) -> DataState:
        return TasksDbDal.update_task(task_id, name, description, deadline)

    @staticmethod
    def delete_task(task_id: int) -> DataState:
        return TasksDbDal.delete_task(task_id)