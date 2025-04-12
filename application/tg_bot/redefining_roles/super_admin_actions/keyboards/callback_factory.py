from aiogram.filters.callback_data import CallbackData


class BackToUsersList(CallbackData, prefix="back_to_users_list"):
    pass

class BackToAdminActions(CallbackData, prefix="back_to_admin_actions"):
    pass