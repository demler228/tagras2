from aiogram.filters.callback_data import CallbackData

class TaskActionCallbackFactory(CallbackData, prefix="task_action"):
    action: str
    task_id: int

class UpdateActionCallbackFactory(CallbackData, prefix="update_action"):
    action: str
    task_id: int
class TaskAdminCallbackFactory(CallbackData, prefix="task_admin"):
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

class PaginationTaskListCallbackFactory(CallbackData, prefix="task_list_pagination"):
    action: str  # "prev_page" или "next_page"
    page: int

class PaginationCallbackFactory(CallbackData, prefix="pagination"):
    action: str  # "prev" или "next"
    page: int    # Номер страницы
    task_id: int # ID задачи

