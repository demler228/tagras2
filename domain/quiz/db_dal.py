import os
import requests
from bs4 import BeautifulSoup
from pdfminer.high_level import extract_text
from docx import Document
from moviepy.video import VideoClip
import whisper
import json
from gigachat import GigaChat
from aiogram.client.session.middlewares.request_logging import logger
from sqlalchemy import select, exists

from application.tg_bot.training.entities.questions import Question
from utils.logs import program_logger
from .models.quiz import QuestionBase, AnswerBase, QuizResult
from domain.training.education.models.theme import ThemeBase
from utils.connection_db import connection_db
from utils.data_state import DataState, DataSuccess, DataFailedMessage
from .modules.utils import remove_empty_lines
from domain.user.models.user import UserBase
from utils.config import settings

auth = settings.SBER_AUTH
giga = GigaChat(
    credentials=auth,
    model='GigaChat:latest',
    verify_ssl_certs=False
)


def process_text(input_text):
    lines = [line.strip() for line in input_text.split('\n') if line.strip()]
    single_line = ' '.join(lines)
    processed_text = ' '.join(single_line.split())
    return processed_text


class FileRepository:
    @staticmethod
    def process_pdf(pdf_path):
        text = extract_text(pdf_path)
        return remove_empty_lines(text)

    @staticmethod
    def process_docx(docx_path):
        doc = Document(docx_path)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return remove_empty_lines(text)

    @staticmethod
    def process_video(video_path, audio_path="audio_temp.mp3"):
        clip = mp.VideoClip(video_path)
        clip.audio.write_audiofile(audio_path, codec="mp3")
        model = whisper.load_model("base")
        result = model.transcribe(audio_path, fp16=False)
        os.remove(audio_path)
        return result["text"]

    @staticmethod
    def process_file(file_path):
        ext = os.path.splitext(file_path)[-1].lower()
        if ext == ".pdf":
            return FileRepository.process_pdf(file_path)
        elif ext == ".mp4":
            return FileRepository.process_video(file_path)
        elif ext == ".docx":
            return FileRepository.process_docx(file_path)
        return None


class WebRepository:
    @staticmethod
    def process_url(url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            for script in soup(["script", "style"]):
                script.decompose()
            text = soup.get_text(separator="\n")
            return process_text(remove_empty_lines(text))[:6000]
        except requests.RequestException as e:
            program_logger.error(e)
            return None


class QuizRepository:
    @staticmethod
    def get_quiz_questions(text):
        payload = f"""
        Сгенерируй 20 вопросов по тексту. Каждый вопрос должен быть в следующем формате:
        - Вопрос
        - 4 варианта ответа (пронумерованные от 1 до 4)
        - Правильный ответ (указанный в формате "Правильный ответ: X)")

        Верни ответ в формате JSON, как в примере ниже:

        [
            {{
                "question": "Почему Бу не смог провести успешные переговоры с американцами?",
                "answers": [
                    "Он не знал английский язык.",
                    "Он не подготовился к переговорам.",
                    "Он не смог договориться с американцами.",
                    "Он не был уверен в себе."
                ],
                "correct_answer": "Он не подготовился к переговорам."
            }}
        ]

        Вот текст: {text}

        Убедись, что ответ строго соответствует этому формату JSON. Не добавляй лишних символов или комментариев.
        """
        try:
            response = giga.chat(payload)
            content = response.choices[0].message.content
            try:
                quiz_data = json.loads(content)
                return DataSuccess(quiz_data)
            except json.JSONDecodeError as e:
                program_logger.error(f"Неверный формат ответа от GigaChat: {e}")
                return DataFailedMessage("Неверный формат ответа от GigaChat")
            except Exception as e:
                program_logger.error(f"Ошибка обработки ответа от GigaChat: {e}")
                return DataFailedMessage("Ошибка обработки ответа от GigaChat")
        except Exception as e:
            program_logger.error(f"Ошибка соединения с GigaChat API: {e}")
            return DataFailedMessage("Ошибка соединения с GigaChat API")

    @staticmethod
    def save_quiz(quiz_data: list, theme_name: str) -> DataState:
        Session = connection_db()
        if Session is None:
            return DataFailedMessage("Ошибка подключения к базе данных")

        with Session() as session:
            try:
                theme = session.query(ThemeBase).filter_by(name=theme_name).first()
                if not theme:
                    theme = ThemeBase(name=theme_name)
                    session.add(theme)
                    session.commit()

                for question_data in quiz_data:
                    question = QuestionBase(
                        text=question_data["question"],
                        theme_id=theme.id
                    )
                    session.add(question)
                    session.flush()

                    correct_answer = AnswerBase(
                        text=question_data["correct_answer"],
                        is_correct=True,
                        question_id=question.id
                    )
                    session.add(correct_answer)

                    for answer_text in question_data["answers"]:
                        if answer_text != question_data["correct_answer"]:
                            answer = AnswerBase(
                                text=answer_text,
                                is_correct=False,
                                question_id=question.id
                            )
                            session.add(answer)

                session.commit()
                return DataSuccess()
            except Exception as e:
                session.rollback()
                program_logger.error(e)
                return DataFailedMessage(f"Ошибка базы данных: {str(e)}")

    @staticmethod
    def get_questions_by_theme(theme_id: int) -> DataState:
        Session = connection_db()
        if Session is None:
            return DataFailedMessage("Ошибка в работе базы данных!")

        with Session() as session:
            try:
                questions_db = session.execute(
                    select(QuestionBase).where(QuestionBase.theme_id == theme_id)
                ).scalars().all()

                result = []
                for question_db in questions_db:
                    answers_db = session.execute(
                        select(AnswerBase).where(AnswerBase.question_id == question_db.id)
                    ).scalars().all()

                    answers = [answer_db.text for answer_db in answers_db]
                    correct_answer = next((answer_db.text for answer_db in answers_db if answer_db.is_correct), None)

                    question_obj = Question(
                        id=question_db.id,
                        theme_id=question_db.theme_id,
                        text=question_db.text,
                        answers=answers,
                        correct_answer=correct_answer
                    )
                    result.append(question_obj)

                return DataSuccess(result)
            except Exception as e:
                program_logger.error(e)
                return DataFailedMessage("Ошибка в работе базы данных!")

    @staticmethod
    def save_quiz_result(user_id: int, theme_id: int, score: int) -> DataState:
        Session = connection_db()
        if Session is None:
            program_logger.error("Ошибка подключения к базе данных")
            return DataFailedMessage("Ошибка подключения к базе данных")

        with Session() as session:
            try:
                user = session.query(UserBase).filter(UserBase.telegram_id == user_id).first()
                if not user:
                    logger.warning(f"Пользователь с telegram_id={user_id} не найден")
                    return DataFailedMessage("Пользователь не найден в базе данных")

                result = QuizResult(
                    user_id=user.id,
                    theme_id=theme_id,
                    score=score
                )
                session.add(result)
                session.commit()

                return DataSuccess()
            except Exception as e:
                session.rollback()
                program_logger.error(e)
                return DataFailedMessage(f"Ошибка сохранения результата: {str(e)}")
