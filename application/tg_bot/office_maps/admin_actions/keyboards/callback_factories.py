from aiogram.filters.callback_data import CallbackData

class BuildingCallbackFactory(CallbackData, prefix="building"):
    building_id: int

class DeleteBuildingCallbackFactory(CallbackData, prefix="delete_building"):
    building_id: int

class ChangeNameBuildingCallbackFactory(CallbackData, prefix="change_name_building"):
    building_id: int

class ChangePhotoBuildingCallbackFactory(CallbackData, prefix="change_photo_building"):
    building_id: int

class FloorCallbackFactory(CallbackData, prefix="floor"):
    building_id: int
    floor_id: int

class SectionCallbackFactory(CallbackData, prefix="section"):
    building_id: int
    floor_id: int
    section_id: int

class BackToBuildingCallbackFactory(CallbackData, prefix="back_to_buildings"):
    pass