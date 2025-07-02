from loguru import logger
import datetime
from domain.user.models.user import UserBase
from sqlalchemy import select

from application.tg_bot.events.entites.event import Event
from domain.events.models.event import EventBase
from domain.events.models.user_events import UserEventBase
from domain.user.models.user import UserBase
from utils.connection_db import connection_db
from utils.data_state import DataState, DataFailedMessage, DataSuccess
from utils.logs import program_logger


class EventDbDal:

    @staticmethod
    def get_events_by_user_id(user_id:int, start_date: datetime, end_date:datetime) -> DataState:
        Session = connection_db()
        if Session is None:
            return DataFailedMessage('Ошибка в работе базы данных!')
        with Session() as session:
            try:
                events =  (
                    session.query(EventBase)
                    .join(UserEventBase, EventBase.id == UserEventBase.event_id)
                    .join(UserBase, UserBase.id == UserEventBase.user_id)
                    .filter(UserBase.id == user_id,
                    EventBase.date >= start_date,
                    EventBase.date <= end_date)).all()

                return DataSuccess(events)
            except Exception as e:
                program_logger.error(e)
                return DataFailedMessage('Ошибка в получении мероприятий!')

    @staticmethod
    def get_all_events_for_week(start_date: datetime, end_date:datetime) -> DataState:
        Session = connection_db()
        if Session is None:
            return DataFailedMessage('Ошибка в работе базы данных!')
        with Session() as session:
            try:
                events =  (
                    session.query(EventBase)
                    .where(EventBase.date >= start_date,
                    EventBase.date <= end_date)).all()

                return DataSuccess(events)
            except Exception as e:
                program_logger.error(e)
                return DataFailedMessage('Ошибка в получении мероприятий!')

    @staticmethod
    def create_event(event: Event) -> DataState:
        Session = connection_db()

        if Session is None:
            return DataFailedMessage('Ошибка в работе базы данных!')
        with Session() as session:
            try:
                event_base = EventBase(name=event.name,description=event.description, date=event.date)
                session.add(event_base)

            except Exception as e:
                session.rollback() # - используйте, если что-то меняете
                program_logger.error(e)
                return DataFailedMessage('Не удалось добавить новое событие!')
            else:
                session.commit() # - используйте, если что-то меняете

                return DataSuccess(event_base.id)

    @staticmethod
    def get_event(event_id:int) -> DataState:
        Session = connection_db()
        if Session is None:
            return DataFailedMessage('Ошибка в работе базы данных!')
        with Session() as session:
            try:
                event_base = session.query(EventBase).get(event_id)

                return DataSuccess(event_base)
            except Exception as e:
                program_logger.error(e)
                return DataFailedMessage('Ошибка в получении события!')

    @staticmethod
    def update_event(event: Event) -> DataState:
        Session = connection_db()

        if Session is None:
            return DataFailedMessage('Ошибка в работе базы данных!')
        with Session() as session:
            try:
                event_base = session.query(EventBase).get(event.id)
                if not event_base:
                    return DataFailedMessage('Мероприятие было было удалено!')

                event_base.name = event.name
                event_base.description = event.description
                event_base.date = event.date

            except Exception as e:
                session.rollback() # - используйте, если что-то меняете
                program_logger.error(e)
                return DataFailedMessage('Ошибка в работе базы данных!')
            else:
                session.commit() # - используйте, если что-то меняете

                return DataSuccess()

    @staticmethod
    def delete_event(event: Event) -> DataState:
        Session = connection_db()

        if Session is None:
            return DataFailedMessage('Ошибка в работе базы данных!')
        with Session() as session:
            try:
                session.query(EventBase).filter(EventBase.id == event.id).delete()
            except Exception as e:
                session.rollback()  # - используйте, если что-то меняете
                program_logger.error(e)
                return DataFailedMessage('Ошибка в удалении мероприятия!')
            else:
                session.commit()  # - используйте, если что-то меняете

                return DataSuccess()

    @staticmethod
    def get_event_members(event_id: int) -> DataState:
        Session = connection_db()
        if Session is None:
            return DataFailedMessage('Ошибка в работе базы данных!')
        with Session() as session:
            try:
                members =  (
                    session.query(UserBase)
                    .join(UserEventBase, UserBase.id == UserEventBase.user_id)
                    .join(EventBase,EventBase.id == UserEventBase.event_id)
                    .filter(EventBase.id == event_id)).all()

                return DataSuccess(members)
            except Exception as e:
                program_logger.error(e)
                return DataFailedMessage('Ошибка в получении участников мероприятия!')

    @staticmethod
    def delete_member(user_id: int, event_id: int) -> DataState:
        Session = connection_db()

        if Session is None:
            return DataFailedMessage('Ошибка в работе базы данных!')
        with Session() as session:
            try:
                session.query(UserEventBase).filter(UserEventBase.user_id == user_id, UserEventBase.event_id == event_id).delete()
            except Exception as e:
                session.rollback()  # - используйте, если что-то меняете
                program_logger.error(e)
                return DataFailedMessage('Ошибка в удалении пользователя из мероприятия!')
            else:
                session.commit()  # - используйте, если что-то меняете

                return DataSuccess()

    @staticmethod
    def add_member(user_id: int, event_id: int) -> DataState:
        Session = connection_db()
        if Session is None:
            return DataFailedMessage('Ошибка в работе базы данных!')
        with Session() as session:
            try:
                user_event_base = UserEventBase(user_id=user_id, event_id=event_id)
                session.add(user_event_base)

            except Exception as e:
                session.rollback() # - используйте, если что-то меняете
                program_logger.error(e)
                return DataFailedMessage('Не удалось добавить пользователя в мероприятие!')
            else:
                session.commit() # - используйте, если что-то меняете

                return DataSuccess()
