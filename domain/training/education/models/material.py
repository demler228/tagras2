from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from utils.base_model import Base


class MaterialBase(Base):
    __tablename__ = "materials"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String)
    url: Mapped[str] = mapped_column(String)

    #чисто для отладки, чтобы в консоли нормально объекты видеть
    def __repr__(self):
        return f"FaqBase(id={self.id}, title={self.title}, url={self.url})"