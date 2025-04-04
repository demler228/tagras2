from aiogram.filters.callback_data import CallbackData

class TaskPersonalCallbackFactory(CallbackData, prefix="task"):
    task_id: int

class BackTasksListCallbackFactory(CallbackData, prefix="back_to_tasks_list"):
    pass
