from aiogram.client.session.middlewares.request_logging import logger
from psycopg2 import Error
from sqlalchemy import select

from application.tg_bot.faq.entities.faq import Faq
from domain.faq.models.faq import FaqBase
from utils.connection_db_old import connection_db as connection_db_old
from utils.connection_db import connection_db
from pydantic import BaseModel

from utils.data_state import DataState, DataSuccess, DataFailedMessage


class FaqDbDal(BaseModel):
    # pyscope не используем
    def get_faq_list_old(self) -> DataState:
        conn = connection_db_old()

        if conn is None:
            return DataFailedMessage('Ошибка в работе базы данных!')
        try:
            with conn.cursor() as cur:
                stmt = "SELECT * FROM faq"
                cur.execute(
                    stmt,
                )
                faq_data = cur.fetchall()
                return DataSuccess(faq_data)
        except Error as e:
            logger.error(e)
            return DataFailedMessage('Ошибка в работе базы данных!')
        finally:
            conn.close()

    def get_faq_list(self) -> DataState:
        Session = connection_db()

        if Session is None:
            return DataFailedMessage('Ошибка в работе базы данных!')
        with Session() as session:
            try:
                statement = select(FaqBase).order_by(FaqBase.id)
                faq_data = session.scalars(statement).all()
                #faq_data = session.query(FaqBase).all()

            except Exception as e:
                #session.rollback() # - используйте, если что-то меняете
                logger.error(e)
                return DataFailedMessage('Ошибка в работе базы данных!')
            else:
                #session.commit() # - используйте, если что-то меняете

                return DataSuccess(faq_data)

    def faq_update(self,faq: Faq) -> DataState:
        Session = connection_db()

        if Session is None:
            return DataFailedMessage('Ошибка в работе базы данных!')
        with Session() as session:
            try:
                faq_base = session.query(FaqBase).get(faq.id)
                if not faq_base:
                    return DataFailedMessage('Вопрос-ответ был удален!')

                faq_base.question = faq.question
                faq_base.answer = faq.answer

            except Exception as e:
                session.rollback() # - используйте, если что-то меняете
                logger.error(e)
                return DataFailedMessage('Ошибка в работе базы данных!')
            else:
                session.commit() # - используйте, если что-то меняете

                return DataSuccess()

    def faq_delete(self,faq: Faq) -> DataState:
        Session = connection_db()

        if Session is None:
            return DataFailedMessage('Ошибка в работе базы данных!')
        with Session() as session:
            try:
                session.query(FaqBase).filter(FaqBase.id == faq.id).delete()

            except Exception as e:
                session.rollback() # - используйте, если что-то меняете
                logger.error(e)
                return DataFailedMessage('Ошибка в работе базы данных!')
            else:
                session.commit() # - используйте, если что-то меняете

                return DataSuccess()

    def faq_create(self,faq: Faq) -> DataState:
        Session = connection_db()

        if Session is None:
            return DataFailedMessage('Ошибка в работе базы данных!')
        with Session() as session:
            try:
                faq_base = FaqBase(question=faq.question,answer=faq.answer)
                session.add(faq_base)

            except Exception as e:
                session.rollback() # - используйте, если что-то меняете
                logger.error(e)
                return DataFailedMessage('Ошибка в работе базы данных!')
            else:
                session.commit() # - используйте, если что-то меняете

                return DataSuccess(faq_base.id)