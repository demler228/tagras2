__all__ = ("router",)

from aiogram import Router
from .admin_actions.handlers.theme_handlers import router as admin_training_handler_routers
from application.tg_bot.training.personal_actions.handlers import router as training_routers
from application.tg_bot.training.personal_actions.education import router as education_routers

router = Router()

router.include_router(admin_training_handler_routers)
router.include_router(training_routers)
router.include_router(education_routers)




