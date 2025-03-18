from aiogram.filters.callback_data import CallbackData

class AdminBuildingCallbackFactory(CallbackData, prefix="admin_building"):
    building_id: int

class AdminFloorCallbackFactory(CallbackData, prefix="admin_floor"):
    building_id: int
    floor_id: int

class AdminSectionCallbackFactory(CallbackData, prefix="admin_section"):
    building_id: int
    floor_id: int
    section_id: int
