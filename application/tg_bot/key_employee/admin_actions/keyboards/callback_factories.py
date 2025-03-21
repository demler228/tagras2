# application/tg_bot/key_employee/admin_actions/keyboards/callback_factories.py
from aiogram.filters.callback_data import CallbackData

class EmployeeCallback(CallbackData, prefix="employee"):
    action: str  # "view", "edit", "delete", "edit_name", "edit_description", "edit_role", "edit_phone", "edit_telegram", "confirm_delete"
    employee_id: int

class PaginationCallback(CallbackData, prefix="paginate"):
    action: str  # "prev", "next"
    page: int

class AdminActionCallback(CallbackData, prefix="admin_action"):
    action: str  # "view", "add", "edit"