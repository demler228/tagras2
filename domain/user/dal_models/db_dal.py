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
    def update_employees_from_1c(employee_data: List[User]) -> DataState:
        Session = connection_db()

        if Session is None:
            return DataFailedMessage("Ошибка в работе базы данных!")

        with Session() as session:
            try:
                for employee in employee_data:
                    existing_user = session.query(UserBase).filter_by(telegram_id=employee.telegram_id).first()

                    if not existing_user:
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
                print(str(e))
                logger.error(f"Database error: {e}")
                return DataFailedMessage("Ошибка при работе с базой данных!")

    @staticmethod
    def get_employee_data_from_1c() -> DataState[List[User]]:
        try:
            employees = {
                "users": [
                    {
                        "id": 1,
                        "telegram_id": 123456789,
                        "username": "john_doe",
                        "phone": "+1234567890",
                        "role": "user",
                        "tg_username": "@john_doe"
                    },
                    {
                        "id": 2,
                        "telegram_id": 987654321,
                        "username": "jane_smith",
                        "phone": "+1987654321",
                        "role": "admin",
                        "tg_username": "@jane_smith"
                    },
                    {
                        "id": 3,
                        "telegram_id": 112233445,
                        "username": "michael_brown",
                        "phone": "+1122334455",
                        "role": "user",
                        "tg_username": "@michael_brown"
                    },
                    {
                        "id": 3,
                        "telegram_id": 865251371,
                        "username": "abdullin ramzil",
                        "phone": "+79374884101",
                        "role": "admin",
                        "tg_username": "@ramzil46"
                    }
                ]
            }

            if "users" not in employees or not isinstance(employees["users"], list):
                raise ValueError("Invalid data format: 'users' key is missing or not a list.")

            user_list = [User(**employee) for employee in employees["users"]]

            return DataSuccess[List[User]](data=user_list)

        except Exception as e:
            return DataFailedMessage(error_message=str(e))

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


