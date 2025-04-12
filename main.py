import asyncio
from typing import Callable, Dict, Any, Awaitable

from aiogram import Bot, Dispatcher, BaseMiddleware
from aiogram.types import Message

from application.tg_bot.middleware import LoggingMiddleware
from utils.config import settings
from application import router
from utils.get_employee_data_from_1c import hourly_request_to_1c
from utils.logs import program_logger


async def main():
    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher()
    dp.callback_query.outer_middleware(LoggingMiddleware())
    dp.include_router(router)
    asyncio.create_task(hourly_request_to_1c())

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":

    program_logger.info('bot started work')
    asyncio.run(main())