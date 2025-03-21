# domain/key_employee/models/key_employee.py
from sqlalchemy import String, Text, BigInteger  # Импортируем BigInteger
from sqlalchemy.orm import Mapped, mapped_column
from utils.base_model import Base

class KeyEmployeeBase(Base):
    __tablename__ = "key_users"

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger)  # Используем BigInteger
    username: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text)
    phone: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(255))

    def __repr__(self):
        return f"KeyEmployee(id={self.id}, telegram_id={self.telegram_id}, username={self.username}, description={self.description}, phone={self.phone}, role={self.role})"