__all__ = ("router",)

from aiogram import Router

from .tg_bot import router as tg_bot_routers

router = Router()

router.include_router(tg_bot_routers)
