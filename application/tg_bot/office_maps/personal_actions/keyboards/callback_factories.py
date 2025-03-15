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

class BackCallbackFactory(CallbackData, prefix="back"):
    action: str  # "to_buildings", "to_floors", "to_menu"
    building_id: int = None  # Для возврата к этажам