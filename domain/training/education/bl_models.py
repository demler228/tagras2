from application.tg_bot.training.entities.theme import Theme
from utils.data_state import DataState
from .dal_models import EducationDAL


class EducationBL(object):
    @staticmethod
    def get_themes()-> DataState:
        return EducationDAL.get_themes()

    @staticmethod
    def get_materials(theme_id: int)-> DataState:
        return EducationDAL.get_materials(theme_id)

    @staticmethod
    def theme_update(theme: Theme) -> DataState:
        data_state = EducationDAL.theme_update(theme)

        return data_state

    @staticmethod
    def theme_create(theme: Theme) -> DataState:
        data_state = EducationDAL.theme_create(theme)

        return data_state

    @staticmethod
    def theme_delete(theme: Theme) -> DataState:
        data_state = EducationDAL.theme_delete(theme)

        return data_state