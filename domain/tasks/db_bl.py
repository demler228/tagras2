import os

from loguru import logger

from application.tg_bot.tasks.entities.task import Task
from application.tg_bot.user.entities.user import User
from .db_dal import TasksDbDal
from utils.data_state import DataSuccess, DataState, DataFailedMessage
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
    def get_all_users() -> DataState[list[User]]:
        data_state = TasksDbDal.get_all_users()
        return data_state

    @staticmethod
    def get_assigned_users_by_task_id(task_id: int) -> DataState[list[User]]:
        data_state = TasksDbDal.get_assigned_users_by_task_id(task_id)
        if isinstance(data_state, DataSuccess):
            return data_state
        else:
            logger.info(f"Состояние присвоенных пользователей {data_state.data}")

    @staticmethod
    def get_all_tasks() -> DataState[list[Task]]:
        data_state = TasksDbDal.get_all_tasks()
        return data_state
    @staticmethod
    def create_task(name: str, description: str, deadline: str = None) -> DataState:
        return TasksDbDal.create_task(name, description, deadline)

    @staticmethod
    def get_task_detail_by_task_id(task_id: int) -> DataState:
        data_state = TasksDbDal.get_task_by_task_id(task_id)
        return data_state

    @staticmethod
    def assign_task_to_user(task_id: int, selected_users: list) -> DataState:
        clear_process_data_state = TasksDbDal.delete_assigned_users_by_task_id(task_id)
        if isinstance(clear_process_data_state, DataSuccess):
            if selected_users is None:
                return DataFailedMessage('Пользователь не найден!')
            else:
                for user_id in selected_users:
                    TasksDbDal.assign_task_to_user(task_id, user_id)
                return DataSuccess("Пользователи успешно присвоены")


    @staticmethod
    def update_task(task_id: int, name: str = None, description: str = None, deadline: str = None) -> DataState:
        return TasksDbDal.update_task(task_id, name, description, deadline)

    @staticmethod
    def delete_task(task_id: int) -> DataState:
        return TasksDbDal.delete_task(task_id)