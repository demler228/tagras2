from aiogram.filters import BaseFilter
from aiogram.types import Message
from loguru import logger
from domain.user.bl_models.db_bl import UserBL
from utils.data_state import DataSuccess


class IsAdminFilter(BaseFilter):
    """
    Filter that checks for admin rights existence
    """

    async def __call__(self, message: Message) -> bool:
        data_state = UserBL.get_user_by_telegram_id(message.from_user.id)
        if isinstance(data_state, DataSuccess):
            return data_state.data.role.endswith('admin')

        logger.error(f'Не получилось проверить пользователя с tg id: {message.from_user.id} на права администратора')
        return False


def is_admin(user_id: int) -> bool:
    data_state = UserBL.get_user_by_telegram_id(user_id)
    if isinstance(data_state, DataSuccess):
        return data_state.data.role.endswith('admin')

    return False


def is_super_admin(user_id: int) -> bool:
    print(f'tdrthdfghedrtfghg_id - {user_id}')
    data_state = UserBL.get_user_by_telegram_id(user_id)
    if isinstance(data_state, DataSuccess):
        return data_state.data.role == 'super_admin'

    return False
