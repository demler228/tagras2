__all__ = ("router",'admin_router')

from aiogram import Router

from .admin_actions import router as admin_handler_routers
from .personal_actions import router as handler_routers

router = Router()
admin_router = Router()

admin_router.include_router(admin_handler_routers)
router.include_router(handler_routers)