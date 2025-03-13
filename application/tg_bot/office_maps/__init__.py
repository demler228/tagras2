__all__ = ("router",)

from aiogram import Router

from application.tg_bot.office_maps.personal_actions.handlers import router as handler_routers

router = Router()

router.include_router(handler_routers)