from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column
from utils.base_model import Base

class KeyEmployeeBase(Base):
    __tablename__ = "key_users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    telegram_username: Mapped[str | None] = mapped_column(String(255), nullable=True)
    username: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text)
    phone: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(255))