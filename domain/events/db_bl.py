from xmlrpc.client import DateTime
from pydantic import BaseModel
from application.tg_bot.events.entites.event import Event
from domain.events.db_dal import EventDbDal
from domain.user.dal_models.db_dal import UserDbDal
from utils.data_state import DataSuccess, DataState



class EventDbBl(BaseModel):

    @staticmethod
    def get_events_by_telegram_id(telegram_id: int, start_date:DateTime, end_date:DateTime) -> DataState[list[Event]]:
        data_state = UserDbDal.get_user_by_telegram_id(telegram_id)
        if isinstance(data_state, DataSuccess):
            user_id = data_state.data.id
            data_state = EventDbDal.get_events_by_user_id(user_id, start_date, end_date)

        return data_state
