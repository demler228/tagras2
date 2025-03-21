__all__ = ("router",)

from aiogram import Router

from .quiz import router as quiz_routers
from .education import router as education_router
from .handlers import router as training_menu_router

router = Router()

router.include_router(quiz_routers)
router.include_router(education_router)
router.include_router(training_menu_router)
