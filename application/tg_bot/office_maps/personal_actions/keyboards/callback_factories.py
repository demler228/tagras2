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

class BackCallbackFactory(CallbackData, prefix="back_to_floor"):
    action: str
    building_id: int = None  # Для возврата к этажам

class BackToBuildingCallbackFactory(CallbackData, prefix="back_to_buildings"):
    pass