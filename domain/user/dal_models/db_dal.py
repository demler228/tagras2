from loguru import logger
from sqlalchemy import select

from domain.user.models.user import UserBase
from utils.connection_db import connection_db
from utils.data_state import DataState, DataFailedMessage, DataSuccess


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
                logger.exception(e)
                return DataFailedMessage('Ошибка в получении пользователя!')