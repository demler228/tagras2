from pydantic import BaseModel
from typing import List

from application.tg_bot.key_employee.entities.key_employee import KeyEmployee
from .db_dal import KeyEmployeeDbDal
from .models.key_employee import KeyEmployeeBase
from utils.data_state import DataSuccess, DataState

class KeyEmployeeDbBl(BaseModel):

    @staticmethod
    def _to_pydantic(employee: KeyEmployeeBase) -> KeyEmployee:
        return KeyEmployee(
            id=employee.id,
            telegram_username=employee.telegram_username,
            username=employee.username,
            description=employee.description,
            phone=employee.phone,
            role=employee.role
        )

    @staticmethod
    def _to_sqlalchemy(employee: KeyEmployee) -> KeyEmployeeBase:
        return KeyEmployeeBase(
            id=employee.id,
            telegram_username=employee.telegram_username,
            username=employee.username,
            description=employee.description,
            phone=employee.phone,
            role=employee.role
        )

    @staticmethod
    def get_key_employee_list() -> DataState:
        data_state = KeyEmployeeDbDal.get_key_employee_list()
        if isinstance(data_state, DataSuccess):
            key_employee_data = data_state.data
            pydantic_employees = [KeyEmployeeDbBl._to_pydantic(employee) for employee in key_employee_data]
            return DataSuccess(pydantic_employees)
        return data_state

    @staticmethod
    def key_employee_update(key_employee: KeyEmployee) -> DataState:
        db_employee = KeyEmployeeDbBl._to_sqlalchemy(key_employee)
        data_state = KeyEmployeeDbDal.key_employee_update(db_employee)
        return data_state

    @staticmethod
    def key_employee_delete(employee_id: int) -> DataState:
        data_state = KeyEmployeeDbDal.key_employee_delete(employee_id)
        return data_state

    @staticmethod
    def key_employee_create(key_employee: KeyEmployee) -> DataState:
        db_employee = KeyEmployeeDbBl._to_sqlalchemy(key_employee)
        data_state = KeyEmployeeDbDal.key_employee_create(db_employee)
        if isinstance(data_state, DataSuccess):
            key_employee.id = db_employee.id
            return DataSuccess(key_employee)
        return data_state