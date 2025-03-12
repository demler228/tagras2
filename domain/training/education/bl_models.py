from .dal_models import EducationDAL


class EducationBL(object):
    @staticmethod
    def get_themes():
        return EducationDAL.get_themes()

    @staticmethod
    def get_materials(theme_id: int):
        return EducationDAL.get_material(theme_id)