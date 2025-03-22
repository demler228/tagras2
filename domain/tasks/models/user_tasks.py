from sqlalchemy import Column, ForeignKey, Integer
from utils.base_model import Base


class UserTaskBase(Base):
    __tablename__ = 'user_tasks'

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    task_id = Column(Integer, ForeignKey('tasks.id'), primary_key=True)
