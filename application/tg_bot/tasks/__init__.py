__all__ = ("router",'admin_router')

from aiogram import Router
from application.tg_bot.tasks.admin_actions.handlers import router as handler_admin_routers
from application.tg_bot.tasks.admin_actions.edit_handler import router as handler_edit_tasks_admin_routers
from application.tg_bot.tasks.admin_actions.delete_task_handlers import router as handler_delete_tasks_admin_routers
from application.tg_bot.tasks.personal_actions.handlers import router as handler_routers


router = Router()
admin_router = Router()
admin_router.include_router(handler_admin_routers)
admin_router.include_router(handler_delete_tasks_admin_routers)
admin_router.include_router(handler_edit_tasks_admin_routers)
router.include_router(handler_routers)