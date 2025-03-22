# db_dal.py
from loguru import logger
from sqlalchemy import select
from sqlalchemy.orm import Session


from application.tg_bot.tasks.entities.task import Task

from domain.tasks.models.tasks import TaskBase
from domain.tasks.models.user_tasks import UserTaskBase
from domain.user.models.user import UserBase

from application.tg_bot.office_maps.entities.building import Building
from application.tg_bot.office_maps.entities.floor import Floor
from application.tg_bot.office_maps.entities.section import Section
from domain.office_maps.models.building import BuildingBase
from domain.office_maps.models.floor import FloorBase
from domain.office_maps.models.section import SectionBase
from utils.connection_db import connection_db
from utils.data_state import DataState, DataSuccess, DataFailedMessage


class TasksDbDal:

    @staticmethod
    def get_tasks_by_user_id(user_id: int) -> DataState:
        Session = connection_db()
        if not Session:
            return DataFailedMessage('Ошибка в работе базы данных!')
        with Session() as session:
            try:
                statement = (select(TaskBase)
                             .join(UserTaskBase, TaskBase.id == UserTaskBase.task_id)
                             .join(UserBase, UserTaskBase.user_id == UserBase.id)
                             .filter(UserTaskBase.user_id == user_id))
                tasks = session.scalars(statement).all()
                return DataSuccess(tasks)
            except Exception as e:
                logger.error(e)
                return DataFailedMessage('Ошибка в работе базы данных!')
