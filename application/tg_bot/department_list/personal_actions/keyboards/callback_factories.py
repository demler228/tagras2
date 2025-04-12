from aiogram.filters.callback_data import CallbackData

# Для отделов
class DepartmentCallback(CallbackData, prefix="department"):
    action: str  # "view"
    department_id: int  # ID отдела

# Для сотрудников в отделе
class DepartmentEmployeeCallback(CallbackData, prefix="department_employee"):
    action: str  # "view"
    employee_id: int  # ID сотрудника

class DepartmentListCallback(CallbackData, prefix="departments_page"):
    action: str  # "page"
    page: int

class DepartmentEmployeePageCallback(CallbackData, prefix="employee_page"):
    department_id: int
    page: int