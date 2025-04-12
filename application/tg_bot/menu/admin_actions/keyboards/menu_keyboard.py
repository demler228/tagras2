from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder




def get_admin_main_menu_keyboard(is_super_admin: bool) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="FAQ", callback_data="faq_button_admin")
    builder.button(text="Мероприятия и встречи", callback_data="events_button_admin")
    builder.button(text="Задачи", callback_data="tasks_button_admin")
    builder.button(text="Карты офиса", callback_data="office_maps_button_admin")
    builder.button(text="Тренинги", callback_data="training_button_admin")
    builder.button(text="Сотрудники", callback_data="employees_button_admin")
    builder.button(text="Ключевые сотрудники", callback_data="contacts_button_admin")
    builder.button(text="Список отделов", callback_data="department_list_button_admin")
    if is_super_admin:
        builder.button(text="Определить роли", callback_data="redefining_roles_super_admin")

    builder.button(text="🔙 Выйти из админ-панели", callback_data="back_to_main_menu")

    builder.adjust(1)

    return builder.as_markup()