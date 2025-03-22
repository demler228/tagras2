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
