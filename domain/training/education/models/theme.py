from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from utils.base_model import Base


class ThemeBase(Base):
    __tablename__ = "themes"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()

    #чисто для отладки, чтобы в консоли нормально объекты видеть
    def __repr__(self):
        return f"ThemeBase(id={self.id}, name={self.name})"