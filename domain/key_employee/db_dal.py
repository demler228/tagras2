from sqlalchemy import select
from pydantic import BaseModel

from utils.logs import program_logger
from .models.key_employee import KeyEmployeeBase
from utils.connection_db import connection_db
from utils.data_state import DataState, DataSuccess, DataFailedMessage

class KeyEmployeeDbDal(BaseModel):

    @staticmethod
    def get_key_employee_list() -> DataState:
        Session = connection_db()
        if Session is None:
            return DataFailedMessage('Ошибка в работе базы данных! Сессия не создалась')
        with Session() as session:
            try:
                statement = select(KeyEmployeeBase).order_by(KeyEmployeeBase.id)
                key_employee_data = session.scalars(statement).all()
                return DataSuccess(key_employee_data)
            except Exception as e:
                program_logger.error(e)
                return DataFailedMessage(f'Ошибка в работе базы данных')

    @staticmethod
    def key_employee_update(key_employee: KeyEmployeeBase) -> DataState:
        Session = connection_db()
        if Session is None:
            return DataFailedMessage('Ошибка в работе базы данных!')
        with Session() as session:
            try:
                key_employee_base = session.query(KeyEmployeeBase).get(key_employee.id)
                if not key_employee_base:
                    return DataFailedMessage('Ключевой сотрудник был удален!')
                key_employee_base.telegram_username = key_employee.telegram_username
                key_employee_base.username = key_employee.username
                key_employee_base.description = key_employee.description
                key_employee_base.phone = key_employee.phone
                key_employee_base.role = key_employee.role
                session.commit()
                return DataSuccess()
            except Exception as e:
                session.rollback()
                program_logger.error(e)
                return DataFailedMessage(f'Ошибка в работе базы данных')

    @staticmethod
    def key_employee_delete(employee_id: int) -> DataState:
        Session = connection_db()
        if Session is None:
            return DataFailedMessage('Ошибка в работе базы данных!')
        with Session() as session:
            try:
                session.query(KeyEmployeeBase).filter(KeyEmployeeBase.id == employee_id).delete()
                session.commit()
                return DataSuccess()
            except Exception as e:
                session.rollback()
                program_logger.error(e)
                return DataFailedMessage(f'Ошибка в работе базы данных')

    @staticmethod
    def key_employee_create(key_employee: KeyEmployeeBase) -> DataState:
        Session = connection_db()
        if Session is None:
            return DataFailedMessage('Ошибка в работе базы данных! Сессия не создалась')
        with Session() as session:
            try:
                session.add(key_employee)
                session.commit()
                return DataSuccess(key_employee.id)
            except Exception as e:
                session.rollback()
                program_logger.error(e)
                return DataFailedMessage(f'Ошибка в работе базы данных')