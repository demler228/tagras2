import asyncio
import sys
from aiogram import Bot, Dispatcher
from loguru import logger
from utils.config import settings
from application import router



async def main():
    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)


    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logger.add(sys.stderr, format="{time} {level} {message}", filter="my_module", level="DEBUG")
    logger.add("file.log")
    logger.info('bot started work')
    asyncio.run(main())