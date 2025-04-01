from aiogram.filters.callback_data import CallbackData

class TaskActionCallbackFactory(CallbackData, prefix="task_action"):
    action: str
    task_id: int

class UpdateActionCallbackFactory(CallbackData, prefix="update_action"):
    action: str
    task_id: int
class TaskAdminCallbackFactory(CallbackData, prefix="task"):
    task_id: int

class BackTasksListAdminCallbackFactory(CallbackData, prefix="back_to_tasks_list_admin"):
    pass

class BackToActionsAdminCallbackFactory(CallbackData, prefix="back_to_tasks_actions"):
    pass
class BackToMenuAdminCallbackFactory(CallbackData, prefix="back_to_admin_main_menu"):
    pass

class UserIdCallbackFactory(CallbackData, prefix="user"):
    user_id: int
    task_id: int


class PaginationCallbackFactory(CallbackData, prefix="pagination"):
    action: str  # "prev" или "next"
    page: int    # Номер страницы
    task_id: int # ID задачи

