from loguru import logger
import datetime
from domain.events.models.event import EventBase
from domain.events.models.user_events import UserEvent
from domain.user.models.user import UserBase
from utils.connection_db import connection_db
from utils.data_state import DataState, DataFailedMessage, DataSuccess


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
                    .join(UserEvent, EventBase.id == UserEvent.event_id)
                    .join(UserBase, UserBase.id == UserEvent.user_id)
                    .filter(UserBase.id == user_id,
                    EventBase.date >= start_date,
                    EventBase.date <= end_date)).all()

                return DataSuccess(events)
            except Exception as e:
                logger.error(e)
                return DataFailedMessage('Ошибка в получении мероприятий!')