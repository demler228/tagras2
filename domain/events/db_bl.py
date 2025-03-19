from xmlrpc.client import DateTime
from pydantic import BaseModel
from application.tg_bot.events.entites.event import Event
from utils.data_state import DataSuccess, DataState



class EventDbBl(BaseModel):

    @staticmethod
    def get_events_by_telegram_id(telegram_id: int, start_date:DateTime, end_date:DateTime) -> DataState[list[Event]]:
        data_state = get_events_by_telegram_id.get_faq_list(telegram_id, start_date,end_date)
        if isinstance(data_state, DataSuccess):
            events = data_state.data
            return DataSuccess(events)

        return data_state
