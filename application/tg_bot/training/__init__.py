__all__ = ("router",)

from aiogram import Router

from .handlers import router as training_routers
from .education import router as education_routers

router = Router()

router.include_router(training_routers)
router.include_router(education_routers)




