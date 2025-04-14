from loguru import logger
from sqlalchemy import select

from application.tg_bot.training.entities.materials import Material
from application.tg_bot.training.entities.theme import Theme
from domain.training.education.models.material import MaterialBase
from domain.training.education.models.theme import ThemeBase
from utils.connection_db import connection_db

from utils.data_state import DataState, DataFailedMessage, DataSuccess
from utils.logs import program_logger


class EducationDAL(object):
    @staticmethod
    def get_themes() -> DataState:
        Session = connection_db()

        if Session is None:
            return DataFailedMessage('Ошибка в работе базы данных!')

        with Session() as session:
            try:
                statement = select(ThemeBase).order_by(ThemeBase.id)
                themes = session.scalars(statement).all()
            except Exception as e:
                program_logger.error(e)
                return DataFailedMessage('Ошибка в работе базы данных!')
            else:
                return DataSuccess(themes)

    @staticmethod
    def get_materials(theme_id: int) -> DataState:
        Session = connection_db()

        if Session is None:
            return DataFailedMessage('Ошибка в работе базы данных!')

        with Session() as session:
            try:
                statement = select(MaterialBase).where(MaterialBase.theme_id == theme_id)
                materials = session.scalars(statement).all()
            except Exception as e:
                program_logger.error(e)
                return DataFailedMessage('Ошибка в работе базы данных!')
            else:
                return DataSuccess(materials)

    @staticmethod
    def theme_update(theme: Theme) -> DataState:
        Session = connection_db()

        if Session is None:
            return DataFailedMessage('Ошибка в работе базы данных!')
        with Session() as session:
            try:
                theme_base = session.query(ThemeBase).get(theme.id)
                if not theme_base:
                    return DataFailedMessage('Вопрос-ответ был удален!')

                theme_base.name = theme.name

            except Exception as e:
                session.rollback()  # - используйте, если что-то меняете
                program_logger.error(e)
                return DataFailedMessage('Ошибка в работе базы данных!')
            else:
                session.commit()  # - используйте, если что-то меняете

                return DataSuccess()

    @staticmethod
    def theme_delete(theme: Theme) -> DataState:
        Session = connection_db()

        if Session is None:
            return DataFailedMessage('Ошибка в работе базы данных!')
        with Session() as session:
            try:
                session.query(ThemeBase).filter(ThemeBase.id == theme.id).delete()

            except Exception as e:
                session.rollback()  # - используйте, если что-то меняете
                program_logger.error(e)
                return DataFailedMessage('Ошибка в работе базы данных!')
            else:
                session.commit()  # - используйте, если что-то меняете

                return DataSuccess()

    @staticmethod
    def theme_create(theme: Theme) -> DataState:
        Session = connection_db()

        if Session is None:
            return DataFailedMessage('Ошибка в работе базы данных!')
        with Session() as session:
            try:
                theme_base = ThemeBase(name=theme.name)
                session.add(theme_base)

            except Exception as e:
                session.rollback()  # - используйте, если что-то меняете
                program_logger.error(e)
                return DataFailedMessage('Ошибка в работе базы данных!')
            else:
                session.commit()  # - используйте, если что-то меняете

                return DataSuccess(theme_base.id)

    @staticmethod
    def material_create(material: Material) -> DataState:
        Session = connection_db()

        if Session is None:
            return DataFailedMessage('Ошибка в работе базы данных!')
        with Session() as session:
            try:
                material_base = MaterialBase(title=material.title,url=material.url,theme_id=material.theme_id)
                session.add(material_base)

            except Exception as e:
                session.rollback()  # - используйте, если что-то меняете
                program_logger.error(e)
                return DataFailedMessage('Ошибка в работе базы данных!')
            else:
                session.commit()  # - используйте, если что-то меняете

                return DataSuccess(material_base.id)

    @staticmethod
    def material_update(material: Material) -> DataState:
        Session = connection_db()

        if Session is None:
            return DataFailedMessage('Ошибка в работе базы данных!')
        with Session() as session:
            try:
                material_base = session.query(MaterialBase).get(material.id)
                if not material_base:
                    return DataFailedMessage('Вопрос-ответ был удален!')

                material_base.title = material.title
                material_base.url = material.url

            except Exception as e:
                session.rollback()  # - используйте, если что-то меняете
                program_logger.error(e)
                return DataFailedMessage('Ошибка в работе базы данных!')
            else:
                session.commit()  # - используйте, если что-то меняете

                return DataSuccess()

    @staticmethod
    def material_delete(material: Material) -> DataState:
        Session = connection_db()

        if Session is None:
            return DataFailedMessage('Ошибка в работе базы данных!')
        with Session() as session:
            try:
                session.query(MaterialBase).filter(MaterialBase.id == material.id).delete()

            except Exception as e:
                session.rollback()  # - используйте, если что-то меняете
                program_logger.error(e)
                return DataFailedMessage('Ошибка в работе базы данных!')
            else:
                session.commit()  # - используйте, если что-то меняете

                return DataSuccess()