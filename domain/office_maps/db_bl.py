# db_bl.py
from .db_dal import BuildingDbDal, FloorDbDal, SectionDbDal
from utils.data_state import DataSuccess, DataState

class BuildingDbBl:

    @staticmethod
    def get_buildings() -> DataState:
        """
        Получает список всех зданий.
        """
        return BuildingDbDal.get_buildings()

    @staticmethod
    def get_building_photo(building_id: int) -> DataState:
        """
        Получает фото здания по ID.
        """
        return BuildingDbDal.get_building_photo(building_id)

class FloorDbBl:

    @staticmethod
    def get_floors_by_building(building_id: int) -> DataState:
        """
        Получает список этажей для конкретного здания.
        """
        return FloorDbDal.get_floors_by_building(building_id)

    @staticmethod
    def get_floor_photo(floor_id: int) -> DataState:
        """
        Получает фото этажа по ID.
        """
        return FloorDbDal.get_floor_photo(floor_id)

class SectionDbBl:

    @staticmethod
    def get_sections_by_floor(floor_id: int) -> DataState:
        """
        Получает список разделов для конкретного этажа.
        """
        return SectionDbDal.get_sections_by_floor(floor_id)

    @staticmethod
    def get_section_photo(section_id: int) -> DataState:
        """
        Получает фото раздела по ID.
        """
        return SectionDbDal.get_section_photo(section_id)