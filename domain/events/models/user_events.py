from sqlalchemy import Column, ForeignKey, Integer
from domain.events.models.event import EventBase
from domain.user.models.user import UserBase
from utils.base_model import Base

class UserEventBase(Base):
    __tablename__ = 'user_events'

    user_id = Column(Integer, ForeignKey(UserBase.id), primary_key=True)
    event_id = Column(Integer, ForeignKey(EventBase.id), primary_key=True)
