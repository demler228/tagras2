__all__ = "router"

from aiogram import Router
from application.tg_bot.redefining_roles.super_admin_actions.handlers import router as handler_super_admin_routers


router = Router()
router.include_router(handler_super_admin_routers)
