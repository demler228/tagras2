from aiogram.filters import BaseFilter
from aiogram.types import Message
from utils.config import settings
class IsAdminFilter(BaseFilter):
    """
    Filter that checks for admin rights existence
    """

    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in settings.OWNERS
