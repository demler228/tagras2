from pydantic import BaseModel
from application.tg_bot.faq.entities.faq import Faq
from domain.faq.db_dal import FaqDbDal
from utils.data_state import DataSuccess, DataState
from utils.table_convertor import to_entity


class FaqDbBl(BaseModel):
    faqDbDal: FaqDbDal

    def get_faq_list(self) -> DataState:
        data_state = self.faqDbDal.get_faq_list()
        if isinstance(data_state, DataSuccess):
            faq_data = data_state.data
            #return DataSuccess(list(map(lambda data: Faq(id=data[0],question=data[1],answer=data[2]),faq_data))) № это с pyscope
            return DataSuccess([to_entity(data, Faq) for data in faq_data])

        return data_state

    def faq_update(self,faq: Faq) -> DataState:
        data_state = self.faqDbDal.faq_update(faq)

        return data_state

    def faq_create(self,faq: Faq) -> DataState:
        data_state = self.faqDbDal.faq_create(faq)

        return data_state

    def faq_delete(self,faq: Faq) -> DataState:
        data_state = self.faqDbDal.faq_delete(faq)

        return data_state
