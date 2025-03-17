# db_bl.py
from application.tg_bot.office_maps.entities.building import Building
from application.tg_bot.office_maps.entities.floor import Floor
from application.tg_bot.office_maps.entities.section import Section
from .db_dal import MapsDbDal
from utils.data_state import DataSuccess, DataState

class MapsDbBl:

    @staticmethod
    def get_buildings() -> DataState:
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
    def delete_building(building_id: int) -> DataState:
        data_state = MapsDbDal.building_delete(building_id)

        return data_state

    @staticmethod
    def delete_floor(floor_id: int) -> DataState:
        data_state = MapsDbDal.floor_delete(floor_id)

        return data_state

    @staticmethod
    def delete_section(section_id: int) -> DataState:
        data_state = MapsDbDal.section_delete(section_id)

        return data_state