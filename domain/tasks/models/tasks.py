from xmlrpc.client import DateTime
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship
from domain.events.models.user_events import UserEventBase
from utils.base_model import Base


class TaskBase(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    creation_date: Mapped[DateTime] = mapped_column(TIMESTAMP(True))
    deadline: Mapped[DateTime] = mapped_column(TIMESTAMP(True))
