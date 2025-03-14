__all__ = ("router",)

from aiogram import Router

from .admin_actions.handlers import router as admin_handler_routers
from .personal_actions.handlers import router as handler_routers

router = Router()

router.include_router(admin_handler_routers)
router.include_router(handler_routers)

