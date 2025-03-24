__all__ = ("router",'admin_router')

from aiogram import Router
from application.tg_bot.training.admin_actions.handlers import router as admin_training_routers
from application.tg_bot.training.personal_actions import router as personal_training_routers

router = Router()
admin_router = Router()

admin_router.include_router(admin_training_routers)
router.include_router(personal_training_routers)




