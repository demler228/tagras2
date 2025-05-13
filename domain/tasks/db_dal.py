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
                session.rollback()
                program_logger.error(e)
                return DataFailedMessage('Ошибка в работе базы данных!')

    @staticmethod
    def get_task_by_task_id(task_id: int) -> DataState:
        Session = connection_db()
        if not Session:
            return DataFailedMessage('Ошибка в работе базы данных!')
        with Session() as session:
            try:
                statement = (select(TaskBase)

                             .filter(TaskBase.id == task_id))
                task = session.scalar(statement)
                return DataSuccess(task)
            except Exception as e:
                program_logger.error(e)
                return DataFailedMessage('Ошибка в работе базы данных!')

    @staticmethod
    def get_all_tasks() -> DataState:
        Session = connection_db()
        if not Session:
            return DataFailedMessage('Ошибка в работе базы данных!')
        with Session() as session:
            try:
                statement = (select(TaskBase)
                             .order_by(TaskBase.id)
                             )
                tasks = session.scalars(statement).all()
                return DataSuccess(tasks)
            except Exception as e:
                session.rollback()
                program_logger.error(e)
                return DataFailedMessage('Ошибка в работе базы данных!')

    @staticmethod
    def get_all_users() -> DataState:
        Session = connection_db()
        if not Session:
            return DataFailedMessage('Ошибка в работе базы данных!')
        with Session() as session:
            try:
                statement = (select(UserBase).order_by(UserBase.username))
                users = session.scalars(statement).all()
                return DataSuccess(users)
            except Exception as e:
                session.rollback()
                program_logger.error(e)
                return DataFailedMessage('Ошибка в работе базы данных!')

    @staticmethod
    def create_task(name: str, description: str, deadline: str = None) -> DataState:
        Session = connection_db()
        if not Session:
            return DataFailedMessage('Ошибка в работе базы данных!')
        with Session() as session:
            try:
                new_task = TaskBase(
                    name=name,
                    description=description,
                    creation_date=datetime.now(),
                    deadline=deadline if deadline else None
                )
                session.add(new_task)
                session.commit()
                session.refresh(new_task)  # Получаем ID созданной задачи
                return DataSuccess(new_task.id)
            except Exception as e:
                session.rollback()
                program_logger.error(e)
                return DataFailedMessage('Ошибка при создании задачи!')

    @staticmethod
    def update_task(task_id: int, name: str = None, description: str = None, deadline: str = None) -> DataState:
        Session = connection_db()
        if not Session:
            return DataFailedMessage('Ошибка в работе базы данных!')
        with Session() as session:
            try:
                task = session.query(TaskBase).filter_by(id=task_id).first()
                if not task:
                    return DataFailedMessage('Задача не найдена!')

                if name:
                    task.name = name
                if description:
                    task.description = description
                if deadline:
                    task.deadline = deadline

                session.commit()
                return DataSuccess()
            except Exception as e:
                session.rollback()
                program_logger.error(e)
                return DataFailedMessage('Ошибка при обновлении задачи!')

    @staticmethod
    def delete_task(task_id: int) -> DataState:
        Session = connection_db()
        if not Session:
            return DataFailedMessage('Ошибка в работе базы данных!')
        with Session() as session:
            try:
                task = session.query(TaskBase).filter_by(id=task_id).first()
                if not task:
                    return DataFailedMessage('Задача не найдена!')

                session.delete(task)
                session.commit()
                return DataSuccess()
            except Exception as e:
                program_logger.error(e)
                session.rollback()
                return DataFailedMessage('Ошибка при удалении задачи!')

    @staticmethod
    def assign_task_to_user(task_id: int, user_id: int) -> DataState:
        Session = connection_db()
        if not Session:
            return DataFailedMessage('Ошибка в работе базы данных!')
        with Session() as session:
            try:
                # Проверяем существование задачи и пользователя
                task = session.query(TaskBase).filter_by(id=task_id).first()
                user = session.query(UserBase).filter_by(id=user_id).first()
                if not task or not user:
                    return DataFailedMessage('Задача или пользователь не найдены!')

                # Создаем связь между задачей и пользователем
                user_task = UserTaskBase(user_id=user_id, task_id=task_id)
                session.add(user_task)
                session.commit()
                return DataSuccess()
            except Exception as e:
                program_logger.error(e)
                session.rollback()
                return DataFailedMessage('Ошибка при присвоении задачи!')

    @staticmethod
    def get_assigned_users_by_task_id(task_id: int) -> DataState:
        Session = connection_db()
        if not Session:
            return DataFailedMessage('Ошибка в работе базы данных!')
        with Session() as session:
            try:
                statement = (
                    select(UserBase)
                    .join(UserTaskBase, UserBase.id == UserTaskBase.user_id)
                    .filter(UserTaskBase.task_id == task_id)
                )
                tasks = session.scalars(statement).all()
                return DataSuccess(tasks)
            except Exception as e:
                session.rollback()
                program_logger.error(e)
                return DataFailedMessage('Ошибка в работе базы данных!')
    @staticmethod
    def delete_assigned_users_by_task_id(task_id: int) -> DataState:
        Session = connection_db()
        if not Session:
            return DataFailedMessage('Ошибка в работе базы данных!')
        with Session() as session:
            try:
                users_tasks = session.query(UserTaskBase).filter_by(task_id=task_id).all()

                if not users_tasks:
                    return DataSuccess(f'Связка пользователей с задачей {task_id} пока не существует')

                # Удаляем каждую запись по отдельности
                for user_task in users_tasks:
                    session.delete(user_task)

                session.commit()
                return DataSuccess()
            except Exception as e:
                session.rollback()
                program_logger.error(e)
                return DataFailedMessage('Ошибка в работе базы данных!')

