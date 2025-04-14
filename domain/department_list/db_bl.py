from pydantic import BaseModel
from typing import List, Optional
from .db_dal import EmployeeDbDal, DepartmentDbDal
from .models import EmployeeModel, DepartmentModel
from utils.data_state import DataSuccess, DataState, DataFailedMessage
from application.tg_bot.department_list.entities import Department, Employee


class EmployeeDbBl(BaseModel):
    @staticmethod
    def _to_pydantic(employee: EmployeeModel) -> "Employee":
        return Employee(
            id=employee.id,
            name=employee.name,
            phone=employee.phone or None,
            description=employee.description or None,
            department_id=employee.department_id,
        )

    @staticmethod
    def _to_sqlalchemy(employee: "Employee") -> EmployeeModel:
        return EmployeeModel(
            id=employee.id,
            name=employee.name,
            phone=employee.phone,
            description=employee.description,
            department_id=employee.department_id,
        )

    @staticmethod
    def get_employee_list(department_id: int | None = None) -> DataState:
        data_state = EmployeeDbDal.get_employee_list(department_id)
        if isinstance(data_state, DataSuccess):
            return DataSuccess(
                [
                    EmployeeDbBl._to_pydantic(e)
                    for e in data_state.data
                    if e is not None  # Защита от None
                ]
            )
        return data_state

    @staticmethod
    def create_employee(employee: "Employee") -> DataState:
        if not employee.name:
            return DataFailedMessage("Employee name cannot be empty")
        if not employee.department_id:
            return DataFailedMessage("Department ID must be specified")
        db_employee = EmployeeDbBl._to_sqlalchemy(employee)
        return EmployeeDbDal.create_employee(db_employee)

    @staticmethod
    def update_employee_field(
        employee_id: int, field: str, value: str | None
    ) -> DataState:
        """Обновление конкретного поля сотрудника"""
        if field not in ["name", "phone", "description"]:
            return DataFailedMessage("Invalid field name")

        if field == "name" and not value:
            return DataFailedMessage("Name cannot be empty")

        # Получаем текущие данные сотрудника
        employee_state = EmployeeDbDal.get_employee_details(employee_id)
        if not isinstance(employee_state, DataSuccess):
            return employee_state

        # Обновляем только нужное поле
        employee = employee_state.data
        setattr(employee, field, value)

        return EmployeeDbDal.update_employee(employee)

    @staticmethod
    def delete_employee(employee_id: int) -> DataState:
        return EmployeeDbDal.delete_employee(employee_id)

    @staticmethod
    def get_employee_details(employee_id: int) -> DataState:
        data_state = EmployeeDbDal.get_employee_details(employee_id)
        if isinstance(data_state, DataSuccess):
            return DataSuccess(EmployeeDbBl._to_pydantic(data_state.data))
        return data_state


class DepartmentDbBl(BaseModel):
    @staticmethod
    def _to_pydantic(department: DepartmentModel) -> "Department":
        return Department(id=department.id, name=department.name)

    @staticmethod
    def _to_sqlalchemy(department: "Department") -> DepartmentModel:
        return DepartmentModel(id=department.id, name=department.name)

    @staticmethod
    def get_department_list() -> DataState:
        data_state = DepartmentDbDal.get_department_list()
        if isinstance(data_state, DataSuccess):
            return DataSuccess(
                [DepartmentDbBl._to_pydantic(d) for d in data_state.data]
            )

        return data_state

    @staticmethod
    def create_department(department: "Department") -> DataState:
        db_department = DepartmentDbBl._to_sqlalchemy(department)
        return DepartmentDbDal.create_department(db_department)

    @staticmethod
    def delete_department(department_id: int) -> DataState:
        return DepartmentDbDal.delete_department(department_id)

    @staticmethod
    def get_department_details(department_id: int) -> DataState:
        data_state = DepartmentDbDal.get_department_details(department_id)
        if isinstance(data_state, DataSuccess):
            return DataSuccess(DepartmentDbBl._to_pydantic(data_state.data))
        return data_state
