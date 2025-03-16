from db_dal import FileRepository, WebRepository, QuizRepository, DBRepository
from models.quiz import QuizData, ThemeCreate, QuizCreate
from typing import Optional


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
        return DBRepository.save_quiz(quiz_data, theme_name)
    @staticmethod
    def get_themes():
        return DBRepository.get_themes()

    @staticmethod
    def get_questions_by_theme(theme_id: int):
        return DBRepository.get_questions_by_theme(theme_id)