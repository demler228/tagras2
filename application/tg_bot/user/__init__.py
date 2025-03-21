__all__ = ("router",)

from aiogram import Router

from .handlers import router as employee_router

router = Router()

router.include_router(employee_router)