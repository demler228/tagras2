from typing import Optional

from domain.training.education.db_bl import EducationBL
from .db_dal import FileRepository, WebRepository, QuizRepository
from .models.quiz import QuizData, ThemeCreate, QuizCreate
from utils.data_state import DataFailedMessage, DataState, DataSuccess
from utils.config import settings


class FileService:
    @staticmethod
    def process_file(file_path: str) -> Optional[str]:
        return FileRepository.process_file(file_path)


class WebService:
    @staticmethod
    def process_url(url: str) -> Optional[str]:
        return WebRepository.process_url(url)


class QuizService:
    @staticmethod
    def generate_quiz(materials: list) -> DataState:
        # Объединяем текст из всех материалов
        combined_text = "\n".join([material.url for material in materials])
        
        # Проверяем наличие токена
        token = settings.SBER_AUTH
        if not token:
            return DataFailedMessage("Не удалось получить токен для GigaChat API")
        
        # Генерируем вопросы
        quiz_data = QuizRepository.get_quiz_questions(combined_text)
        if not isinstance(quiz_data, DataSuccess):
            return quiz_data
        
        # Сохраняем вопросы в базу
        theme_name = materials[0].theme.name if materials else "Общая тема"
        save_result = QuizRepository.save_quiz(quiz_data.data, theme_name)
        return save_result


class DBService:
    @staticmethod
    def save_quiz(quiz_data: list, theme_name: str) -> DataState:
        return QuizRepository.save_quiz(quiz_data, theme_name)

    @staticmethod
    def get_themes():
        return EducationBL.get_themes()

    @staticmethod
    def get_questions_by_theme(theme_id: int):
        return QuizRepository.get_questions_by_theme(theme_id)