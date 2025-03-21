__all__ = ("router",)

from aiogram import Router

from .handlers import router as ai_router

router = Router()

router.include_router(ai_router)