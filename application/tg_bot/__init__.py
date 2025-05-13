__all__ = ("router","admin_router")

from aiogram import Router, F
from application.tg_bot.user import router as employee_router
from application.tg_bot.contacts.user import router as user_routers
from application.tg_bot.menu import router as menu_routers
from application.tg_bot.menu import admin_router as menu_admin_routers
from application.tg_bot.faq import router as faq_routers
# from application.tg_bot.events import router as event_routers
from application.tg_bot.office_maps import router as office_maps_routers
# from application.tg_bot.tasks import router as tasks_routers
from application.tg_bot.faq import admin_router as faq_admin_routers
# from application.tg_bot.events import admin_router as event_admin_routers
from application.tg_bot.office_maps import admin_router as office_admin_maps_routers
# from application.tg_bot.tasks import admin_router as tasks_admin_routers
from application.tg_bot.ai_assistant import router as ai_assistant_router
from application.tg_bot.training import router as training_router
from application.tg_bot.training import admin_router as training_admin_router
from application.tg_bot.key_employee import admin_router as key_employee_admin_routers
from application.tg_bot.key_employee import router as key_employee_routers
from application.tg_bot.useful_contacts import router as useful_contacts_routers
from application.tg_bot.department_list import router as department_list_routers
from application.tg_bot.department_list import admin_router as department_list_admin_routers
# from application.tg_bot.redefining_roles import router as redefining_roles_routers
from application.tg_bot.filters.is_admin import IsAdminFilter
router = Router()

admin_router = Router()
admin_router.message.filter(F.chat.type == "private", IsAdminFilter()) # allow bot admin actions only for bot owner
admin_router.callback_query.filter(IsAdminFilter())
admin_router.include_router(employee_router)
admin_router.include_router(menu_admin_routers)
# admin_router.include_router(event_admin_routers)
admin_router.include_router(faq_admin_routers)
admin_router.include_router(key_employee_admin_routers)
# admin_router.include_router(tasks_admin_routers)
# admin_router.include_router(redefining_roles_routers)
admin_router.include_router(office_admin_maps_routers)
admin_router.include_router(training_admin_router)
admin_router.include_router(department_list_admin_routers)

router.include_router(admin_router)
router.include_router(user_routers)
router.include_router(menu_routers)
# router.include_router(event_routers)
router.include_router(faq_routers)
router.include_router(key_employee_routers)
router.include_router(department_list_routers)
router.include_router(useful_contacts_routers)
# router.include_router(tasks_routers)
router.include_router(office_maps_routers)
router.include_router(ai_assistant_router)
router.include_router(training_router)


