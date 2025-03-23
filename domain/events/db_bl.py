from datetime import datetime
from pydantic import BaseModel
from application.tg_bot.events.entites.event import Event
from application.tg_bot.events.entites.userMember import UserMember
from application.tg_bot.user.entities.user import User
from domain.events.db_dal import EventDbDal
from domain.user.dal_models.db_dal import UserDbDal
from utils.data_state import DataSuccess, DataState



class EventDbBl(BaseModel):

    @staticmethod
    def get_events_by_telegram_id(telegram_id: int, start_date:datetime, end_date:datetime) -> DataState[list[Event]]:
        data_state = UserDbDal.get_user_by_telegram_id(telegram_id)
        if isinstance(data_state, DataSuccess):
            user_id = data_state.data.id
            data_state = EventDbDal.get_events_by_user_id(user_id, start_date, end_date)

        return data_state

    @staticmethod
    def get_all_events_for_week(start_date:datetime, end_date:datetime) -> DataState[list[Event]]:
        data_state = EventDbDal.get_all_events_for_week(start_date, end_date)

        return data_state


    @staticmethod
    def create_event(event: Event) -> DataState[int]:
        data_state = EventDbDal.create_event(event)

        return data_state

    @staticmethod
    def get_event(event_id: int) -> DataState[Event]:
        data_state = EventDbDal.get_event(event_id)

        return data_state

    @staticmethod
    def delete_event(event: Event) -> DataState:
        data_state = EventDbDal.delete_event(event)

        return data_state

    @staticmethod
    def update_event(event: Event) -> DataState[Event]:
        data_state = EventDbDal.update_event(event)

        return data_state

    @staticmethod
    def get_event_members(event_id: int) -> DataState[list[User]]:
        data_state = EventDbDal.get_event_members(event_id)

        return data_state

    @staticmethod
    def get_users_by_name(username: str, event_id: int) -> DataState[list[UserMember]]:
        data_state = UserDbDal.get_users_by_name(username)
        if isinstance(data_state, DataSuccess):
            users = data_state.data
            data_state = EventDbDal.get_event_members(event_id)
            if isinstance(data_state, DataSuccess):
                members = data_state.data
                user_members = list(map(lambda user:  UserMember(id=user.id,telegram_id=user.telegram_id, tg_username=user.tg_username,username=user.username,phone=user.phone,role=user.role,is_member=user.id in [member.id for member in members]), users))
                return DataSuccess(user_members)

        return data_state

    @staticmethod
    def change_member_state(member_id: int,is_member:bool, event: Event) -> DataState:
        if is_member:
            data_state = EventDbDal.delete_member(member_id, event.id)
        else:
            data_state = EventDbDal.add_member(member_id, event.id)

        return data_state