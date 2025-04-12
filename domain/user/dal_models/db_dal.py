from loguru import logger
from sqlalchemy import select
from typing import List
from datetime import datetime

from domain.user.models.user import UserBase
from utils.connection_db import connection_db
from utils.data_state import DataState, DataFailedMessage, DataSuccess
from application.tg_bot.user.entities.user import User


class UserDbDal:
    @staticmethod
    def delete_employee(employee_id: int) -> DataState:
        Session = connection_db()
        if Session is None:
            return DataFailedMessage("Ошибка подключения к базе данных!")
        with Session() as session:
            try:
                employee = session.query(UserBase).filter_by(id=employee_id).first()
                if not employee:
                    return DataFailedMessage("Сотрудник не найден!")
                session.delete(employee)
                session.commit()
                return DataSuccess()
            except Exception as e:
                session.rollback()
                logger.error(f"Ошибка при удалении сотрудника: {e}")
                return DataFailedMessage("Ошибка при работе с базой данных!")


    @staticmethod
    def update_employee(employee_id: int, updates: dict) -> DataState:
        Session = connection_db()

        if Session is None:
            return DataFailedMessage("Ошибка подключения к базе данных!")

        with Session() as session:
            try:
                employee = session.query(UserBase).filter_by(id=employee_id).first()
                if not employee:
                    return DataFailedMessage("Сотрудник не найден!")

                for field, value in updates.items():
                    if hasattr(employee, field):
                        setattr(employee, field, value)

                session.commit()
                return DataSuccess()

            except Exception as e:
                session.rollback()
                logger.error(f"Ошибка при обновлении данных сотрудника: {e}")
                return DataFailedMessage("Ошибка при работе с базой данных!")

    @staticmethod
    def get_employee_by_id(employee_id):
        Session = connection_db()

        if Session is None:
            return DataFailedMessage("Ошибка подключения к базе данных!")

        with Session() as session:
            try:
                employee = session.query(UserBase).filter_by(id=employee_id).first()
                if not employee:
                    return DataFailedMessage("Сотрудник не найден!")

                user = User(
                    id=employee.id,
                    telegram_id=employee.telegram_id,
                    tg_username=employee.tg_username,
                    username=employee.username,
                    phone=employee.phone,
                    role=employee.role
                )

                return DataSuccess(data=user)

            except Exception as e:
                logger.error(f"Ошибка при получении данных сотрудника: {e}")
                return DataFailedMessage("Ошибка при работе с базой данных!")

    @staticmethod
    def get_all_employees() -> DataState[List[User]]:
        Session = connection_db()

        if Session is None:
            return DataFailedMessage("Ошибка подключения к базе данных!")

        with Session() as session:
            try:
                employees = session.query(UserBase).all()

                employee_list = [
                    User(
                        id=employee.id,
                        telegram_id=employee.telegram_id,
                        tg_username=employee.tg_username,
                        username=employee.username,
                        phone=employee.phone,
                        role=employee.role
                    )
                    for employee in employees
                ]


                return DataSuccess(data=employee_list)

            except Exception as e:
                logger.error(f"Ошибка при получении списка сотрудников: {e}")
                return DataFailedMessage("Ошибка при работе с базой данных!")


    @staticmethod
    def get_user_by_telegram_id(telegram_id: int) -> DataState:
        Session = connection_db()
        if Session is None:
            return DataFailedMessage('Ошибка в работе базы данных!')
        with Session() as session:
            try:
                statement = select(UserBase).where(UserBase.telegram_id == telegram_id)
                user = session.scalars(statement).one()
                return DataSuccess(user)
            except Exception as e:
                logger.error(e)
                return DataFailedMessage('Ошибка в получении пользователя!')

    @staticmethod
    def add_employee(employee: User) -> DataState:
        Session = connection_db()

        if Session is None:
            return DataFailedMessage("Ошибка в работе базы данных!")

        with Session() as session:
            try:
                existing_user = session.query(UserBase).filter_by(telegram_id=employee.telegram_id).first()

                if existing_user:
                    return DataFailedMessage("Пользователь с таким Telegram ID уже существует!")

                new_user = UserBase(
                    telegram_id=employee.telegram_id,
                    username=employee.username,
                    phone=employee.phone,
                    role=employee.role,
                    created_at=datetime.now(),
                    tg_username=employee.tg_username
                )
                session.add(new_user)
                session.commit()
                return DataSuccess()

            except Exception as e:
                session.rollback()
                logger.error(f"Database error: {e}")
                return DataFailedMessage("Ошибка при работе с базой данных!")

    @staticmethod
    def get_users_by_name(username: str) -> DataState:
        Session = connection_db()
        if Session is None:
            return DataFailedMessage('Ошибка в работе базы данных!')
        with Session() as session:
            try:
                statement = select(UserBase).where(UserBase.username.ilike(f'%{username}%'))
                users = session.scalars(statement).all()
                return DataSuccess(users)
            except Exception as e:
                logger.exception(e)
                return DataFailedMessage('Ошибка в получении пользователей!')


