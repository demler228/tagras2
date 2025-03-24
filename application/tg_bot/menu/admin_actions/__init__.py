__all__ = ("admin_router",)

from aiogram import Router
from application.tg_bot.menu.admin_actions.handlers import router as admin_actions_router

admin_router = Router()

admin_router.include_router(admin_actions_router)
