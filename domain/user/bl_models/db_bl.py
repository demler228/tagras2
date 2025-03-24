from domain.user.dal_models.db_dal import UserDbDal
from utils.data_state import DataState, DataSuccess, DataFailedMessage


class UserBL():
    @staticmethod
    def get_employee_data_from_1c() -> DataState:
        data_state = UserDbDal.get_employee_data_from_1c()

        if isinstance(data_state, DataSuccess):
            return DataSuccess(data_state.data)
        else:
            return DataFailedMessage("Произошла ошибка при обновлении информации сотрудников из базы 1С")

    @staticmethod
    async def update_employee_data() -> DataState:
        employee = UserBL.get_employee_data_from_1c()
        data_state = UserDbDal.update_employees_from_1c(employee.data)

        if isinstance(data_state, DataSuccess):
            return DataSuccess()
        else:
            return DataFailedMessage("Произошла ошибка при обновлении информации сотрудников из базы 1С")




