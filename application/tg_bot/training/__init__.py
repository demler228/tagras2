__all__ = ("router",)

from aiogram import Router
from application.tg_bot.training.admin_actions.handlers import router as admin_training_handler_routers
from application.tg_bot.training.personal_actions.handlers import router as training_routers
from application.tg_bot.training.personal_actions.education import router as education_routers
from application.tg_bot.training.personal_actions.quiz.handlers import router as quiz_router

router = Router()

router.include_router(admin_training_handler_routers)
router.include_router(training_routers)
router.include_router(education_routers)
router.include_router(quiz_router)




