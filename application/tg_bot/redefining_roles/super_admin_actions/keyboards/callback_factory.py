from aiogram.filters.callback_data import CallbackData


class BackToUsersList(CallbackData, prefix="back_to_users_list"):
    pass


class BackToAdminActions(CallbackData, prefix="back_to_admin_main_menu"):
    pass


class MakeRemoveAdminAction(CallbackData, prefix="super_admin_tools"):
    action: str
    user_id: int


