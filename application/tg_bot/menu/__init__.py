__all__ = ("router",)

from aiogram import Router
from application.tg_bot.menu.personal_actions.handlers import router as handler_routers
from application.tg_bot.menu.admin_actions import router as admin_actions_routers

router = Router()

router.include_router(admin_actions_routers)
router.include_router(handler_routers)
