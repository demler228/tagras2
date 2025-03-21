from aiogram.filters.callback_data import CallbackData

class TaskCallbackFactory(CallbackData, prefix="task"):
    task_id: int