from aiogram import Router, F, types
from utils.data_state import DataSuccess
from domain.user.bl_models.db_bl import UserBL

router = Router()

@router.callback_query(F.data == "update_user_information")
async def update_employee_data(callback_query: types.CallbackQuery):
    data_state = UserBL.update_employee_data()

    if isinstance(data_state, DataSuccess):
        await callback_query.message.answer("Данные о сотрудниках из базы 1С успешно обновлены!")
    else:
        await callback_query.message.answer("Произошла ошибка при обновлении информации сотрудников из базы 1С")