from aiogram.filters.callback_data import CallbackData

class AdminActionCallback(CallbackData, prefix="admin_action"):
    action: str  # Действие: "view_departments", "add_department", "edit_department", "delete_department", и т.д.
