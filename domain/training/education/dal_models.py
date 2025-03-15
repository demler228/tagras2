from loguru import logger
from sqlalchemy import select

from application.tg_bot.training.entities.theme import Theme
from domain.training.education.models.material import MaterialBase
from domain.training.education.models.theme import ThemeBase
from utils.connection_db import connection_db
import psycopg2

from utils.data_state import DataState, DataFailedMessage, DataSuccess


class EducationDAL(object):
    @staticmethod
    def get_themes() -> DataState:
        Session = connection_db()

        if Session is None:
            return DataFailedMessage('Ошибка в работе базы данных!')
        with Session() as session:
            try:
                statement = select(ThemeBase).order_by(ThemeBase.id)
                faq_data = session.scalars(statement).all()
                #faq_data = session.query(FaqBase).all()

            except Exception as e:
                #session.rollback() # - используйте, если что-то меняете
                logger.error(e)
                return DataFailedMessage('Ошибка в работе базы данных!')
            else:
                #session.commit() # - используйте, если что-то меняете

                return DataSuccess(faq_data)

    @staticmethod
    def get_materials(theme_id: int) -> DataState:
        Session = connection_db()

        if Session is None:
            return DataFailedMessage('Ошибка в работе базы данных!')
        with Session() as session:
            try:
                statement = select(MaterialBase).where(ThemeBase.id == theme_id).order_by(MaterialBase.id)
                faq_data = session.scalars(statement).all()
                #faq_data = session.query(FaqBase).all()

            except Exception as e:
                #session.rollback() # - используйте, если что-то меняете
                logger.error(e)
                return DataFailedMessage('Ошибка в работе базы данных!')
            else:
                #session.commit() # - используйте, если что-то меняете

                return DataSuccess(faq_data)

    @staticmethod
    def theme_update(theme: Theme) -> DataState:
        Session = connection_db()

        if Session is None:
            return DataFailedMessage('Ошибка в работе базы данных!')
        with Session() as session:
            try:
                faq_base = session.query(ThemeBase).get(theme.id)
                if not faq_base:
                    return DataFailedMessage('Вопрос-ответ был удален!')

                faq_base.question = theme.name

            except Exception as e:
                session.rollback()  # - используйте, если что-то меняете
                logger.error(e)
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
                logger.error(e)
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
                faq_base = ThemeBase(theme=theme.name)
                session.add(faq_base)

            except Exception as e:
                session.rollback()  # - используйте, если что-то меняете
                logger.error(e)
                return DataFailedMessage('Ошибка в работе базы данных!')
            else:
                session.commit()  # - используйте, если что-то меняете

                return DataSuccess(faq_base.id)