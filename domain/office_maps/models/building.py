from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from utils.base_model import Base

class BuildingBase(Base):
    __tablename__ = "buildings"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    photo_path: Mapped[str] = mapped_column(String, nullable=True)  # Путь к фото