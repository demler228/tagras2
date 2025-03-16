# Models/buildings.py
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from utils.base_model import Base

class Building(Base):
    __tablename__ = "buildings"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    photo_path: Mapped[str] = mapped_column(String, nullable=True)  # Путь к фото

class Floor(Base):
    __tablename__ = "floors"

    id: Mapped[int] = mapped_column(primary_key=True)
    building_id: Mapped[int] = mapped_column(ForeignKey("buildings.id"))
    name: Mapped[str] = mapped_column(String)
    photo_path: Mapped[str] = mapped_column(String, nullable=True)  # Путь к фото

class Section(Base):
    __tablename__ = "sections"

    id: Mapped[int] = mapped_column(primary_key=True)
    floor_id: Mapped[int] = mapped_column(ForeignKey("floors.id"))
    name: Mapped[str] = mapped_column(String)
    photo_path: Mapped[str] = mapped_column(String, nullable=True)  # Путь к фото