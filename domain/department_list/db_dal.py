from typing import Optional
from sqlalchemy import select
from .models import EmployeeModel, DepartmentModel
from utils.connection_db import connection_db
from utils.data_state import DataState, DataSuccess, DataFailedMessage
from sqlalchemy.orm import joinedload

class EmployeeDbDal:
    @staticmethod
    def get_employee_list(department_id: int | None = None) -> DataState:
        Session = connection_db()
        if not Session:
            return DataFailedMessage("Ошибка подключения к БД")

        with Session() as session:
            try:
                stmt = select(EmployeeModel)

                if department_id is not None:
                    stmt = stmt.where(EmployeeModel.department_id == department_id)

                employees = session.scalars(stmt.order_by(EmployeeModel.id)).all()
                return DataSuccess(employees)
            except Exception as e:
                return DataFailedMessage(f"Ошибка БД: {str(e)}")

    @staticmethod
    def create_employee(employee: EmployeeModel) -> DataState:
        Session = connection_db()
        if not Session:
            return DataFailedMessage("Database connection error")

        with Session() as session:
            try:
                session.add(employee)
                session.commit()
                session.refresh(employee)
                return DataSuccess(employee.id)
            except Exception as e:
                session.rollback()
                return DataFailedMessage(f"Database error: {str(e)}")

    @staticmethod
    def update_employee(employee: EmployeeModel) -> DataState:
        Session = connection_db()
        if not Session:
            return DataFailedMessage("Database connection error")

        with Session() as session:
            try:
                db_employee = session.get(EmployeeModel, employee.id)
                if not db_employee:
                    return DataFailedMessage("Employee not found")

                # Обновляем только измененные поля
                for field in ["name", "phone", "description"]:
                    new_value = getattr(employee, field)
                    setattr(db_employee, field, new_value)

                session.commit()
                return DataSuccess()
            except Exception as e:
                session.rollback()
                return DataFailedMessage(f"Database error: {str(e)}")

    @staticmethod
    def delete_employee(employee_id: int) -> DataState:
        Session = connection_db()
        if not Session:
            return DataFailedMessage("Database connection error")

        with Session() as session:
            try:
                employee = session.get(EmployeeModel, employee_id)
                if not employee:
                    return DataFailedMessage("Employee not found")

                session.delete(employee)
                session.commit()
                return DataSuccess()
            except Exception as e:
                session.rollback()
                return DataFailedMessage(f"Database error: {str(e)}")

    @staticmethod
    def get_employee_details(employee_id: int) -> DataState:
        Session = connection_db()
        if not Session:
            return DataFailedMessage("Ошибка подключения к БД")

        with Session() as session:
            try:
                employee = session.get(EmployeeModel, employee_id)

                if not employee:
                    return DataFailedMessage("Сотрудник не найден")

                return DataSuccess(employee)
            except Exception as e:
                return DataFailedMessage(f"Ошибка БД: {str(e)}")


class DepartmentDbDal:
    @staticmethod
    def get_department_list() -> DataState:
        Session = connection_db()
        if not Session:
            return DataFailedMessage("Database connection error")
        with Session() as session:
            try:
                stmt = select(DepartmentModel).order_by(DepartmentModel.id)
                departments = session.scalars(stmt).all()
                return DataSuccess(departments)
            except Exception as e:
                return DataFailedMessage(f"Database error: {e}")

    @staticmethod
    def create_department(department: DepartmentModel) -> DataState:
        Session = connection_db()
        if not Session:
            return DataFailedMessage("Database connection error")
        with Session() as session:
            try:
                session.add(department)
                session.commit()
                session.refresh(department)
                return DataSuccess(department.id)
            except Exception as e:
                session.rollback()
                return DataFailedMessage(f"Database error: {e}")

    @staticmethod
    def delete_department(department_id: int) -> DataState:
        Session = connection_db()
        if not Session:
            return DataFailedMessage("Database connection error")

        with Session() as session:
            try:
                # Проверяем существование отдела
                department = session.get(DepartmentModel, department_id)
                if not department:
                    return DataFailedMessage("Department not found")

                # Удаляем отдел (сотрудники удалятся каскадно, если настроено)
                session.delete(department)
                session.commit()
                return DataSuccess()

            except Exception as e:
                session.rollback()
                return DataFailedMessage(f"Database error: {str(e)}")

    @staticmethod
    def get_department_details(department_id: int) -> DataState:
        Session = connection_db()
        if not Session:
            return DataFailedMessage("Database connection error")

        with Session() as session:
            try:
                department = session.get(DepartmentModel, department_id)
                if not department:
                    return DataFailedMessage("Department not found")
                return DataSuccess(department)
            except Exception as e:
                return DataFailedMessage(f"Database error: {str(e)}")
