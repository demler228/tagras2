from aiogram import Router, types, F
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery
from .keyboards import get_faq_answer_keyboard, get_faq_keyboard
from utils.data_state import DataSuccess, DataState
from domain.faq.db_dal import FaqDbDal
from .keyboards.callback_factories import FaqCallbackFactory, BackToMenuCallbackFactory

router = Router()

@router.callback_query(F.data == "faq_button")
async def handle_faq_button(callback_query: types.CallbackQuery):
    """
    Обрабатывает нажатие на кнопку FAQ.
    """
    faq_items = FaqDbDal().get_faq_list()
    if isinstance(faq_items, DataSuccess):
        await callback_query.message.answer(
            "Выберите интересующий вас вопрос:",
            reply_markup=get_faq_keyboard(page=1, total_questions=len(faq_items.data), questions=faq_items.data)
        )
    else:
        await callback_query.message.answer("Вопросы не найдены.")


@router.callback_query(FaqCallbackFactory.filter())
async def faq_callback_handler(callback_query: CallbackQuery, callback_data: FaqCallbackFactory):
    """
    Обрабатывает нажатия на кнопки FAQ (показ ответа, переход между страницами).
    """
    faq_items = FaqDbDal().get_faq_list()
    if not isinstance(faq_items, DataSuccess):
        await callback_query.message.answer("Ошибка при получении данных.")
        return

    faq_items = faq_items.data

    if callback_data.action == "show":
        question = faq_items[callback_data.question_index]
        await callback_query.message.edit_text(
            f"<b>❓{question.question}</b>\n\n☑️{question.answer}",
            reply_markup=get_faq_answer_keyboard(page=callback_data.page, question_index=callback_data.question_index),
            parse_mode=ParseMode.HTML
        )
    elif callback_data.action in ["back", "next", "prev"]:
        await callback_query.message.edit_text(
            "Выберите интересующий вас вопрос:",
            reply_markup=get_faq_keyboard(page=callback_data.page, total_questions=len(faq_items), questions=faq_items)
        )

    await callback_query.answer()  # Подтверждение обработки callback


@router.callback_query(BackToMenuCallbackFactory.filter())
async def back_to_menu_callback_handler(callback_query: CallbackQuery):
    """
    Возвращает обратно в меню
    """
    await callback_query.message.delete()