from aiogram.filters.callback_data import CallbackData

# Для действий, связанных с сотрудниками
class UserEmployeeCallback(CallbackData, prefix="user_employee"):
    action: str  # "view"
    employee_id: int  # Обязательное поле

# Для пагинации
class UserPaginationCallback(CallbackData, prefix="user_pagination"):
    action: str  # "prev", "next"
    page: int  # Текущая страница