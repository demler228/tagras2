# db_dal.py
from loguru import logger
from sqlalchemy import select
from sqlalchemy.orm import Session


from application.tg_bot.tasks.entities.task import Task

from domain.tasks.models.tasks import TaskBase

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
    def get_tasks() -> DataState:
        Session = connection_db()
        if not Session:
            return DataFailedMessage('Ошибка в работе базы данных!')
        with Session() as session:
            try:
                statement = select(TaskBase)
                tasks = session.scalars(statement).all()
                return DataSuccess(tasks)
            except Exception as e:
                logger.error(e)
                return DataFailedMessage('Ошибка в работе базы данных!')