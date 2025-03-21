from sqlalchemy import Column, ForeignKey, Integer
from utils.base_model import Base


class UserEvent(Base):
    __tablename__ = 'user_events'

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    event_id = Column(Integer, ForeignKey('events.id'), primary_key=True)
