from typing import Optional

from domain.training.education.bl_models import EducationBL
from .db_dal import FileRepository, WebRepository, QuizRepository, QuizDAL
from .models.quiz import QuizData, ThemeCreate, QuizCreate



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
    def generate_quiz(token: str, text: str) -> Optional[dict]:
        return QuizRepository.get_quiz_questions(token, text)


class DBService:
    @staticmethod
    def save_quiz(quiz_data: list, theme_name: str) -> bool:
        return QuizDAL.save_quiz(quiz_data, theme_name)

    @staticmethod
    def get_themes():
        return EducationBL.get_themes()

    @staticmethod
    def get_questions_by_theme(theme_id: int):
        return QuizDAL.get_questions_by_theme(theme_id)