from pydantic import BaseModel

from application.tg_bot.key_employee.entities.key_employee import KeyEmployee
from .db_dal import KeyEmployeeDbDal
from .models.key_employee import KeyEmployeeBase
from utils.data_state import DataSuccess, DataState
from utils.table_convertor import to_entity

class KeyEmployeeDbBl(BaseModel):

    @staticmethod
    def get_key_employee_list() -> DataState:
        data_state = KeyEmployeeDbDal.get_key_employee_list()
        if isinstance(data_state, DataSuccess):
            key_employee_data = data_state.data
            return DataSuccess([to_entity(data, KeyEmployee) for data in key_employee_data])
        return data_state

    @staticmethod
    def key_employee_update(key_employee: KeyEmployeeBase) -> DataState:
        data_state = KeyEmployeeDbDal.key_employee_update(key_employee)
        return data_state

    @staticmethod
    def key_employee_delete(key_employee: KeyEmployeeBase) -> DataState:
        data_state = KeyEmployeeDbDal.key_employee_delete(key_employee)
        return data_state

    @staticmethod
    def key_employee_create(key_employee: KeyEmployee) -> DataState:
        # Создаём объект SQLAlchemy-модели
        db_employee = KeyEmployeeBase(
            telegram_id=key_employee.telegram_id,
            username=key_employee.username,
            description=key_employee.description,
            phone=key_employee.phone,
            role=key_employee.role
        )
        data_state = KeyEmployeeDbDal.key_employee_create(db_employee)
        return data_state