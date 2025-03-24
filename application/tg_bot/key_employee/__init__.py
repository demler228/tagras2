__all__ = ("router",'admin_router')

from aiogram import Router

from .admin_actions import handlers_router as admin_handler_router
from .admin_actions import handlers_edit_router as admin_edit_router
from .personal_actions import router as handler_routers

router = Router()
admin_router = Router()

admin_router.include_router(admin_handler_router)
admin_router.include_router(admin_edit_router)
router.include_router(handler_routers)