from application.tg_bot.user.entities.user import User
from domain.user.dal_models.db_dal import UserDbDal
from utils.data_state import DataState, DataSuccess, DataFailedMessage
from utils.employees_from_1c.telethon_client import get_user_id_by_username


class UserBL:
    @staticmethod
    def delete_employee(employee_id: int) -> DataState:
        return UserDbDal.delete_employee(employee_id)

    @staticmethod
    def update_employee(employee_id: int, updates: dict) -> DataState:
        return UserDbDal.update_employee(employee_id, updates)

    @staticmethod
    def get_employee_by_id(employee_id):
        data_state = UserDbDal.get_employee_by_id(employee_id)

        return data_state

    @staticmethod
    def get_all_employees():
        data_state = UserDbDal.get_all_employees()

        return data_state

    @staticmethod
    async def add_employee(user: User) -> DataState:
        user.telegram_id = await get_user_id_by_username(user.tg_username)
        data_state = UserDbDal.add_employee(user)

        return data_state

    @staticmethod
    def get_user_by_telegram_id(telegram_id: int) -> DataState[User]:
        data_state = UserDbDal.get_user_by_telegram_id(telegram_id)

        return data_state



