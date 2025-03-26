from aiogram.filters.callback_data import CallbackData

class TaskActionCallbackFactory(CallbackData, prefix="task_action"):
    action: str  # "edit", "reassign", "delete"
    task_id: int

class TaskAdminCallbackFactory(CallbackData, prefix="task"):
    task_id: int

class BackTasksListAdminCallbackFactory(CallbackData, prefix="back_to_tasks_list_admin"):
    pass

class BackToTasksActionsAdminCallbackFactory(CallbackData, prefix="back_to_actions_admin"):
    pass

class BackToMenuAdminCallbackFactory(CallbackData, prefix="back_to_admin_main_menu"):
    pass


