__all__ = ("router",)

from aiogram import Router

from .personal_actions import router as handler_routers

router = Router()

router.include_router(handler_routers)