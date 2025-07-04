# db_bl.py
import os

from loguru import logger

from application.tg_bot.office_maps.entities.building import Building
from application.tg_bot.office_maps.entities.floor import Floor
from application.tg_bot.office_maps.entities.section import Section
from .db_dal import MapsDbDal
from utils.data_state import DataSuccess, DataState

class MapsDbBl:

    @staticmethod
    def get_buildings() -> DataState[list[Building]]:
        """
        Получает список всех зданий.
        """
        return MapsDbDal.get_buildings()

    @staticmethod
    def get_building_photo(building_id: int) -> DataState:
        """
        Получает фото здания по ID.
        """
        return MapsDbDal.get_building_photo(building_id)

    @staticmethod
    def get_floors_by_building(building_id: int) -> DataState:
        """
        Получает список этажей для конкретного здания.
        """
        return MapsDbDal.get_floors_by_building(building_id)

    @staticmethod
    def get_floor_photo(floor_id: int) -> DataState:
        """
        Получает фото этажа по ID.
        """
        return MapsDbDal.get_floor_photo(floor_id)

    @staticmethod
    def get_sections_by_floor(floor_id: int) -> DataState:
        """
        Получает список разделов для конкретного этажа.
        """
        return MapsDbDal.get_sections_by_floor(floor_id)

    @staticmethod
    def get_section_photo(section_id: int) -> DataState:
        """
        Получает фото раздела по ID.
        """
        return MapsDbDal.get_section_photo(section_id)

    @staticmethod
    def create_building(building: Building) -> DataState:
        data_state = MapsDbDal.create_building(building)

        return data_state

    @staticmethod
    def create_floor(floor: Floor) -> DataState:
        data_state = MapsDbDal.create_floor(floor)

        return data_state

    @staticmethod
    def create_section(section: Section) -> DataState:
        data_state = MapsDbDal.create_section(section)

        return data_state

    @staticmethod
    def delete_building(building: Building) -> DataState:
        photos_path = [building.photo_path]
        # получаем список всех изображений принадлежащих этому зданию
        data_state = MapsDbDal.get_floors_by_building(building_id=building.id)
        if not data_state.data:
            logger.error('Не удалось получить этажи')
        for floor in data_state.data:
            photos_path.append(floor.photo_path)
            data_state = MapsDbDal.get_sections_by_floor(floor_id=floor.id)
            if not data_state.data:
                logger.error('Не удалось получить отделы')
            for section in data_state.data:
                photos_path.append(section.photo_path)

        data_state = MapsDbDal.building_delete(building)
        if isinstance(data_state, DataSuccess):
            for photo_path in photos_path:
                if os.path.exists(photo_path):
                    os.remove(photo_path)

        return data_state

    @staticmethod
    def delete_floor(floor: Floor) -> DataState:
        photos_path = [floor.photo_path]
        # получаем список всех изображений принадлежащих этому этажу
        data_state = MapsDbDal.get_sections_by_floor(floor_id=floor.id)
        if data_state.data:
            logger.error('Не удалось получить отделы')
        for section in data_state.data:
            photos_path.append(section.photo_path)

        data_state = MapsDbDal.floor_delete(floor)
        if isinstance(data_state, DataSuccess):
            for photo_path in photos_path:
                if os.path.exists(photo_path):
                    os.remove(photo_path)

        return data_state

    @staticmethod
    def delete_section(section: Section) -> DataState:
        data_state = MapsDbDal.section_delete(section)
        if isinstance(data_state, DataSuccess):
            try:
                os.remove(section.photo_path)
            except Exception as ex:
                logger.error(f'Ошибка удаления изображений \n{ex}')
        return data_state

    @staticmethod
    def update_building(building: Building) -> DataState:
        data_state = MapsDbDal.update_building(building)

        return data_state

    @staticmethod
    def update_floor(floor: Floor) -> DataState:
        data_state = MapsDbDal.update_floor(floor)

        return data_state

    @staticmethod
    def update_section(section: Section) -> DataState:
        data_state = MapsDbDal.update_section(section)

        return data_state