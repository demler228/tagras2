# db_dal.py
from loguru import logger
from sqlalchemy import select
from sqlalchemy.orm import Session

from application.tg_bot.office_maps.entities.building import Building
from application.tg_bot.office_maps.entities.floor import Floor
from application.tg_bot.office_maps.entities.section import Section
from domain.office_maps.models.building import BuildingBase
from domain.office_maps.models.floor import FloorBase
from domain.office_maps.models.section import SectionBase
from utils.connection_db import connection_db
from utils.data_state import DataState, DataSuccess, DataFailedMessage
from utils.logs import program_logger


class MapsDbDal:

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
                statement = select(BuildingBase)
                buildings = session.scalars(statement).all()
                return DataSuccess(buildings)
            except Exception as e:
                program_logger.error(e)
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
                statement = select(BuildingBase.photo_path).where(BuildingBase.id == building_id)
                photo_path = session.scalar(statement)
                if photo_path:
                    return DataSuccess(photo_path)
                else:
                    return DataFailedMessage('Фото здания не найдено!')
            except Exception as e:
                program_logger.error(e)
                return DataFailedMessage('Ошибка в работе базы данных!')

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
                statement = select(FloorBase).where(FloorBase.building_id == building_id)
                floors = session.scalars(statement).all()
                return DataSuccess(floors)
            except Exception as e:
                program_logger.error(e)
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
                statement = select(FloorBase.photo_path).where(FloorBase.id == floor_id)
                photo_path = session.scalar(statement)
                if photo_path:
                    return DataSuccess(photo_path)
                else:
                    return DataFailedMessage('Фото этажа не найдено!')
            except Exception as e:
                program_logger.error(e)
                return DataFailedMessage('Ошибка в работе базы данных!')

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
                statement = select(SectionBase).where(SectionBase.floor_id == floor_id)
                sections = session.scalars(statement).all()
                return DataSuccess(sections)
            except Exception as e:
                program_logger.error(e)
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
                statement = select(SectionBase.photo_path).where(SectionBase.id == section_id)
                photo_path = session.scalar(statement)
                if photo_path:
                    return DataSuccess(photo_path)
                else:
                    return DataFailedMessage('Фото раздела не найдено!')
            except Exception as e:
                program_logger.error(e)
                return DataFailedMessage('Ошибка в работе базы данных!')

    @staticmethod
    def create_building(building: Building) -> DataState:
        Session = connection_db()

        if Session is None:
            return DataFailedMessage('Ошибка в работе базы данных!')
        with Session() as session:
            try:
                building_base = BuildingBase(name=building.name,photo_path=building.photo_path)
                session.add(building_base)

            except Exception as e:
                session.rollback() # - используйте, если что-то меняете
                program_logger.error(e)
                return DataFailedMessage('Не удалось добавить новое здание!')
            else:
                session.commit() # - используйте, если что-то меняете

                return DataSuccess(building_base.id)

    @staticmethod
    def create_floor(floor: Floor) -> DataState:
        Session = connection_db()

        if Session is None:
            return DataFailedMessage('Ошибка в работе базы данных!')
        with Session() as session:
            try:
                floor_base = FloorBase(name=floor.name,photo_path=floor.photo_path,building_id=floor.building_id)
                session.add(floor_base)

            except Exception as e:
                session.rollback() # - используйте, если что-то меняете
                program_logger.error(e)
                return DataFailedMessage('Не удалось добавить новый этаж!')
            else:
                session.commit() # - используйте, если что-то меняете

                return DataSuccess(floor_base.id)

    @staticmethod
    def create_section(section: Section) -> DataState:
        Session = connection_db()

        if Session is None:
            return DataFailedMessage('Ошибка в работе базы данных!')
        with Session() as session:
            try:
                section_base = SectionBase(name=section.name,photo_path=section.photo_path,floor_id=section.floor_id)
                session.add(section_base)

            except Exception as e:
                session.rollback() # - используйте, если что-то меняете
                program_logger.error(e)
                return DataFailedMessage('Не удалось добавить новый отдел!')
            else:
                session.commit() # - используйте, если что-то меняете

                return DataSuccess(section_base.id)

    @staticmethod
    def building_delete(building: Building) -> DataState:
        Session = connection_db()

        if Session is None:
            return DataFailedMessage('Ошибка в работе базы данных!')
        with Session() as session:
            try:
                session.query(BuildingBase).filter(BuildingBase.id == building.id).delete()

            except Exception as e:
                session.rollback()  # - используйте, если что-то меняете
                program_logger.error(e)
                return DataFailedMessage('Ошибка в удалении здания!')
            else:
                session.commit()  # - используйте, если что-то меняете

                return DataSuccess()

    @staticmethod
    def floor_delete(floor: Floor) -> DataState:
        Session = connection_db()

        if Session is None:
            return DataFailedMessage('Ошибка в работе базы данных!')
        with Session() as session:
            try:
                session.query(FloorBase).filter(FloorBase.id == floor.id).delete()

            except Exception as e:
                session.rollback()  # - используйте, если что-то меняете
                program_logger.error(e)
                return DataFailedMessage('Ошибка в удалении этажа!')
            else:
                session.commit()  # - используйте, если что-то меняете

                return DataSuccess()

    @staticmethod
    def section_delete(section: Section) -> DataState:
        Session = connection_db()

        if Session is None:
            return DataFailedMessage('Ошибка в работе базы данных!')
        with Session() as session:
            try:
                session.query(SectionBase).filter(SectionBase.id == section.id).delete()

            except Exception as e:
                session.rollback()  # - используйте, если что-то меняете
                program_logger.error(e)
                return DataFailedMessage('Ошибка в удалении отдела!')
            else:
                session.commit()  # - используйте, если что-то меняете

                return DataSuccess()

    @staticmethod
    def update_building(building: Building) -> DataState:
        Session = connection_db()

        if Session is None:
            return DataFailedMessage('Ошибка в работе базы данных!')
        with Session() as session:
            try:
                building_base = session.query(BuildingBase).get(building.id)
                if not building_base:
                    return DataFailedMessage('Здание было удалено!')

                building_base.name = building.name
                building_base.photo_path = building.photo_path

            except Exception as e:
                session.rollback() # - используйте, если что-то меняете
                program_logger.error(e)
                return DataFailedMessage('Ошибка в работе базы данных!')
            else:
                session.commit() # - используйте, если что-то меняете

                return DataSuccess()

    @staticmethod
    def update_floor(floor: Floor) -> DataState:
        Session = connection_db()

        if Session is None:
            return DataFailedMessage('Ошибка в работе базы данных!')
        with Session() as session:
            try:
                floor_base = session.query(FloorBase).get(floor.id)
                if not floor_base:
                    return DataFailedMessage('Этаж был удален!')

                floor_base.name = floor.name
                floor_base.photo_path = floor.photo_path

            except Exception as e:
                session.rollback() # - используйте, если что-то меняете
                program_logger.error(e)
                return DataFailedMessage('Ошибка в работе базы данных!')
            else:
                session.commit() # - используйте, если что-то меняете

                return DataSuccess()

    @staticmethod
    def update_section(section: Section) -> DataState:
        Session = connection_db()

        if Session is None:
            return DataFailedMessage('Ошибка в работе базы данных!')
        with Session() as session:
            try:
                section_base = session.query(SectionBase).get(section.id)
                if not section_base:
                    return DataFailedMessage('Отдел был удален!')

                section_base.name = section.name
                section_base.photo_path = section.photo_path

            except Exception as e:
                session.rollback() # - используйте, если что-то меняете
                program_logger.error(e)
                return DataFailedMessage('Ошибка в работе базы данных!')
            else:
                session.commit() # - используйте, если что-то меняете

                return DataSuccess()
