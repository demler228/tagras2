# db_dal.py
from sqlalchemy import select
from sqlalchemy.orm import Session
from .models.office_maps import Building, Floor, Section
from utils.connection_db import connection_db
from utils.data_state import DataState, DataSuccess, DataFailedMessage

class BuildingDbDal:

    @staticmethod
    def get_buildings() -> DataState:
        """
        Получает список всех зданий.
        """
        Session = connection_db()
        if Session is None:
            return DataFailedMessage('Ошибка в работе базы данных!')
        with Session() as session:
            try:
                statement = select(Building)
                buildings = session.scalars(statement).all()
                return DataSuccess(buildings)
            except Exception as e:
                logger.error(e)
                return DataFailedMessage('Ошибка в работе базы данных!')

    @staticmethod
    def get_building_photo(building_id: int) -> DataState:
        """
        Получает фото здания по ID.
        """
        Session = connection_db()
        if Session is None:
            return DataFailedMessage('Ошибка в работе базы данных!')
        with Session() as session:
            try:
                statement = select(Building.photo_path).where(Building.id == building_id)
                photo_path = session.scalar(statement)
                if photo_path:
                    return DataSuccess(photo_path)
                else:
                    return DataFailedMessage('Фото здания не найдено!')
            except Exception as e:
                logger.error(e)
                return DataFailedMessage('Ошибка в работе базы данных!')

class FloorDbDal:

    @staticmethod
    def get_floors_by_building(building_id: int) -> DataState:
        """
        Получает список этажей для конкретного здания.
        """
        Session = connection_db()
        if Session is None:
            return DataFailedMessage('Ошибка в работе базы данных!')
        with Session() as session:
            try:
                statement = select(Floor).where(Floor.building_id == building_id)
                floors = session.scalars(statement).all()
                return DataSuccess(floors)
            except Exception as e:
                logger.error(e)
                return DataFailedMessage('Ошибка в работе базы данных!')

    @staticmethod
    def get_floor_photo(floor_id: int) -> DataState:
        """
        Получает фото этажа по ID.
        """
        Session = connection_db()
        if Session is None:
            return DataFailedMessage('Ошибка в работе базы данных!')
        with Session() as session:
            try:
                statement = select(Floor.photo_path).where(Floor.id == floor_id)
                photo_path = session.scalar(statement)
                if photo_path:
                    return DataSuccess(photo_path)
                else:
                    return DataFailedMessage('Фото этажа не найдено!')
            except Exception as e:
                logger.error(e)
                return DataFailedMessage('Ошибка в работе базы данных!')

class SectionDbDal:

    @staticmethod
    def get_sections_by_floor(floor_id: int) -> DataState:
        """
        Получает список разделов для конкретного этажа.
        """
        Session = connection_db()
        if Session is None:
            return DataFailedMessage('Ошибка в работе базы данных!')
        with Session() as session:
            try:
                statement = select(Section).where(Section.floor_id == floor_id)
                sections = session.scalars(statement).all()
                return DataSuccess(sections)
            except Exception as e:
                logger.error(e)
                return DataFailedMessage('Ошибка в работе базы данных!')

    @staticmethod
    def get_section_photo(section_id: int) -> DataState:
        """
        Получает фото раздела по ID.
        """
        Session = connection_db()
        if Session is None:
            return DataFailedMessage('Ошибка в работе базы данных!')
        with Session() as session:
            try:
                statement = select(Section.photo_path).where(Section.id == section_id)
                photo_path = session.scalar(statement)
                if photo_path:
                    return DataSuccess(photo_path)
                else:
                    return DataFailedMessage('Фото раздела не найдено!')
            except Exception as e:
                logger.error(e)
                return DataFailedMessage('Ошибка в работе базы данных!')