from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message

from application.tg_bot.filters.is_admin import IsAdminFilter
from utils.logs import user_logger

class LoggingMiddleware(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ):
        if not IsAdminFilter():
            user_logger.info(f"{event.message.chat.full_name}({event.message.chat.id})  pressed handler: {event.data}")
        return await handler(event, data)