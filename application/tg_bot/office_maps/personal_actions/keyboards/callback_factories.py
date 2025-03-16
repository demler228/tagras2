from aiogram.filters.callback_data import CallbackData

class BuildingCallbackFactory(CallbackData, prefix="building"):
    building_id: int

class FloorCallbackFactory(CallbackData, prefix="floor"):
    building_id: int
    floor_id: int

class SectionCallbackFactory(CallbackData, prefix="section"):
    building_id: int
    floor_id: int
    section_id: int

class BackToSectionCallbackFactory(CallbackData, prefix="back_to_sections"):
    building_id: int
    floor_id: int

class BackToFloorCallbackFactory(CallbackData, prefix="back_to_floor"):
    building_id: int

class BackToBuildingCallbackFactory(CallbackData, prefix="back_to_buildings"):
    pass