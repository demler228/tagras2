__all__ = ("router",)

from aiogram import Router

from application.tg_bot.user import router as employee_router
from application.tg_bot.menu.admin_actions.handlers import router as admin_actions_router

router = Router()

router.include_router(admin_actions_router)
router.include_router(employee_router)