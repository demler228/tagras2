from aiogram.filters.callback_data import CallbackData

class AdminDepartmentListCallback(CallbackData, prefix="admin_departments_page"):
    action: str
    page: int

class AdminDepartmentCallback(CallbackData, prefix="admin_department"):
    action: str
    department_id: int

class AdminDepartmentEmployeeCallback(CallbackData, prefix="admin_employee"):
    action: str
    employee_id: int

class AdminDepartmentEmployeePageCallback(CallbackData, prefix="admin_employee_page"):
    department_id: int
    page: int

class AdminConfirmCallback(CallbackData, prefix="admin_confirm"):
    target: str  # department | employee
    entity_id: int

class AdminEmployeeEditFieldCallback(CallbackData, prefix="admin_edit_field"):
    field: str
    employee_id: int
