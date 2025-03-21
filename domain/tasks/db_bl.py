# db_bl.py
import os

from loguru import logger

from application.tg_bot.tasks.entities.task import Task
from application.tg_bot.tasks.entities.user_tasks import UserTask
from .db_dal import TasksDbDal
from utils.data_state import DataSuccess, DataState

class TasksDbBl:

    @staticmethod
    def get_tasks() -> DataState[list[Task]]:
        return TasksDbDal.get_tasks()