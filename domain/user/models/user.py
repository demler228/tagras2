import enum
from xmlrpc.client import DateTime

from sqlalchemy import String, DATETIME, Integer, Enum
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship

from domain.events.models.user_events import UserEvent
from utils.base_model import Base

# class MyEnum(enum.Enum):
#     user = 0
#     admin = 1

class UserBase(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(Integer)
    username: Mapped[str] = mapped_column(String)
    phone: Mapped[str] = mapped_column(String)
    created_at: Mapped[DateTime] = mapped_column(TIMESTAMP(True))
    role: Mapped[str] = mapped_column(Enum('user','admin'))

