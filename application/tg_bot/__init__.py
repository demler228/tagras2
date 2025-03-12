__all__ = ("router",)

from aiogram import Router

from application.tg_bot.contacts.user import router as user_routers
from application.tg_bot.menu import router as menu_routers
from application.tg_bot.faq import router as faq_routers
from application.tg_bot.office_maps import router as office_maps_routers
from application.tg_bot.ai_assistant import router as ai_assistant_router
from application.tg_bot.training import router as training_router


router = Router()

router.include_router(user_routers)
router.include_router(menu_routers)
router.include_router(faq_routers)
router.include_router(office_maps_routers)
router.include_router(ai_assistant_router)
router.include_router(training_router)

