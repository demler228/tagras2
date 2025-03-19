from xmlrpc.client import DateTime

from sqlalchemy import String, DATETIME
from sqlalchemy.orm import Mapped, mapped_column
from utils.base_model import Base


class EventBase(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    date: Mapped[DateTime] = mapped_column(DATETIME)

    #чисто для отладки, чтобы в консоли нормально объекты видеть
    def __repr__(self):
        return f"FaqBase(id={self.id}, question={self.question}, answer={self.answer})"