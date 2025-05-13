# db_dal.py
from datetime import datetime

from loguru import logger
from sqlalchemy import select
from sqlalchemy.orm import Session

from application.tg_bot.tasks.entities.task import Task

from domain.tasks.models.tasks import TaskBase
from domain.tasks.models.user_tasks import UserTaskBase
from domain.user.models.user import UserBase

from utils.connection_db import connection_db
from utils.data_state import DataState, DataSuccess, DataFailedMessage
from utils.logs import program_logger


class RedefiningDbDal:

    @staticmethod
    def get_all_users() -> DataState:
        Session = connection_db()
        if not Session:
            return DataFailedMessage('Ошибка в работе базы данных!')
        with Session() as session:
            try:
                statement = (select(UserBase)
                             .filter(UserBase.role != "super_admin")
                             .order_by(UserBase.role, UserBase.username))
                users = session.scalars(statement).all()
                return DataSuccess(users)
            except Exception as e:
                session.rollback()
                program_logger.error(e)
                return DataFailedMessage('Ошибка в работе базы данных!')
    @staticmethod
    def get_user_info_by_user_id(user_id: int) -> DataState :
        Session = connection_db()
        if not Session:
            return DataFailedMessage('Ошибка в работе базы данных!')
        with Session() as session:
            try:
                statement = (select(UserBase)
                             .filter(UserBase.id == user_id))
                users = session.scalars(statement).first()
                return DataSuccess(users)
            except Exception as e:
                session.rollback()
                program_logger.error(e)
                return DataFailedMessage('Ошибка в работе базы данных!')


    @staticmethod
    def change_user_role(user_id: int, new_role: str) -> DataState:
        Session = connection_db()
        if not Session:
            return DataFailedMessage('Ошибка в работе базы данных!')
        with Session() as session:
            try:
                user = session.query(UserBase).filter(UserBase.id == user_id).first()
                if not user:
                    return DataFailedMessage('Пользователь не найден!')

                # Изменяем роль пользователя
                user.role = new_role
                session.commit()
                return DataSuccess(f"Роль пользователя {user.username} успешно изменена на {new_role}.")
            except Exception as e:
                session.rollback()
                program_logger.error(e)
                return DataFailedMessage('Ошибка при изменении роли пользователя!')



