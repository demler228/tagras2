import os

from loguru import logger

from application.tg_bot.tasks.entities.task import Task
from application.tg_bot.user.entities.user import User
from .db_dal import RedefiningDbDal
from utils.data_state import DataSuccess, DataState, DataFailedMessage
from ..user.dal_models.db_dal import UserDbDal


class RedefinigDbBl:

    @staticmethod
    def get_all_users() -> DataState[list[User]]:
        data_state = RedefiningDbDal.get_all_users()
        return data_state

    @staticmethod
    def change_user_role(user_id: int, new_role: str) -> DataState:
        change = RedefiningDbDal.change_user_role(user_id, new_role)
        if isinstance(change, DataSuccess):
            updated_user_data_state = RedefiningDbDal.get_user_info_by_user_id(user_id)
            return DataSuccess(updated_user_data_state.data)
        else:
            return DataFailedMessage("Произошла ошибка при обновлении информации сотрудников при смене роли")