from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from utils.base_model import Base


class FaqBase(Base):
    __tablename__ = "faq"

    id: Mapped[int] = mapped_column(primary_key=True)
    question: Mapped[str] = mapped_column(String)
    answer: Mapped[str] = mapped_column(String)

    #чисто для отладки, чтобы в консоли нормально объекты видеть
    def __repr__(self):
        return f"FaqBase(id={self.id}, question={self.question}, answer={self.answer})"