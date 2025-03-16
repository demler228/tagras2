import os
import requests
from bs4 import BeautifulSoup
from pdfminer.high_level import extract_text
from docx import Document
import moviepy as mp
import whisper
import json
import uuid
from modules.utils import remove_empty_lines
from sqlalchemy import select
from sqlalchemy.orm import Session
from models.quiz import Theme, Question, Answer
from utils.connection_db import connection_db
from utils.data_state import DataState, DataSuccess, DataFailedMessage
from aiogram.client.session.middlewares.request_logging import logger

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
        clip = mp.VideoFileClip(video_path)
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
            return remove_empty_lines(text)
        except requests.RequestException as e:
            print(f"Ошибка при загрузке страницы: {e}")
            return None

class QuizRepository:
    client_id = "ce7d7680-4bf7-4ff3-b172-3be3794aa5b8"
    secret = "338c3cfd-1038-4d2b-9e27-5af3a3d7f728"
    auth = "Y2U3ZDc2ODAtNGJmNy00ZmYzLWIxNzItM2JlMzc5NGFhNWI4OjMzOGMzY2ZkLTEwMzgtNGQyYi05ZTI3LTVhZjNhM2Q3ZjcyOA=="

    @staticmethod
    def get_token(scope="GIGACHAT_API_PERS"):
        rq_uid = str(uuid.uuid4())
        url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
            "RqUID": rq_uid,
            "Authorization": f"Basic {QuizRepository.auth}",
        }
        payload = {"scope": scope}
        try:
            response = requests.post(url, headers=headers, data=payload, verify=False)
            return response.json().get("access_token", None)
        except requests.RequestException as e:
            print(f"Ошибка: {str(e)}")
            return None

    @staticmethod
    def get_quiz_questions(auth_token, text):
        url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
        payload = json.dumps(
            {
                "model": "GigaChat",
                "messages": [
                    {
                        "role": "user",
                        "content": f"""
    Сгенерируй 10 вопросов по тексту. Каждый вопрос должен быть в следующем формате:
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
        }},

    Вот текст: {text}

    Убедись, что ответ строго соответствует этому формату JSON. Не добавляй лишних символов или комментариев.""",
                    }
                ],
                "temperature": 1,
                "top_p": 0.1,
                "n": 1,
                "stream": False,
                "max_tokens": 2048,
                "repetition_penalty": 1,
                "update_interval": 0,
            }
        )
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {auth_token}",
        }
        try:
            response = requests.post(url, headers=headers, data=payload, verify=False)
            return response.json()
        except requests.RequestException as e:
            print(f"Произошла ошибка: {str(e)}")
            return None

class DBRepository:
    @staticmethod
    def save_quiz(quiz_data: list, theme_name: str) -> DataState:
        Session = connection_db()

        if Session is None:
            return DataFailedMessage("Ошибка в работе базы данных!")
        
        with Session() as session:
            try:
                theme = Theme(theme_name=theme_name)
                session.add(theme)
                session.commit()

                for question_data in quiz_data:
                    question = Question(
                        question_text=question_data["question"],
                        theme_id=theme.id
                    )
                    session.add(question)
                    session.commit()

                    correct_answer = Answer(
                        answer_text=question_data["correct_answer"],
                        is_correct=True,
                        question_id=question.id
                    )
                    session.add(correct_answer)

                    for incorrect_answer in question_data["incorrect_answers"]:
                        answer = Answer(
                            answer_text=incorrect_answer,
                            is_correct=False,
                            question_id=question.id
                        )
                        session.add(answer)

                session.commit()
                return DataSuccess()
            except Exception as e:
                session.rollback()
                logger.error(e)
                return DataFailedMessage("Ошибка в работе базы данных!")

    @staticmethod
    def get_themes() -> DataState:
        Session = connection_db()

        if Session is None:
            return DataFailedMessage("Ошибка в работе базы данных!")
        
        with Session() as session:
            try:
                themes = session.execute(select(Theme)).scalars().all()
                return DataSuccess([{"id": theme.id, "theme_name": theme.theme_name} for theme in themes])
            except Exception as e:
                logger.error(e)
                return DataFailedMessage("Ошибка в работе базы данных!")

    @staticmethod
    def get_questions_by_theme(theme_id: int) -> DataState:
        Session = connection_db()

        if Session is None:
            return DataFailedMessage("Ошибка в работе базы данных!")
        
        with Session() as session:
            try:
                questions = session.execute(
                    select(Question).where(Question.theme_id == theme_id)
                ).scalars().all()

                result = []
                for question in questions:
                    answers = session.execute(
                        select(Answer).where(Answer.question_id == question.id)
                    ).scalars().all()

                    result.append({
                        "question_text": question.question_text,
                        "answers": [answer.answer_text for answer in answers],
                        "correct_answer": next(
                            answer.answer_text for answer in answers if answer.is_correct
                        ),
                    })

                return DataSuccess(result)
            except Exception as e:
                logger.error(e)
                return DataFailedMessage("Ошибка в работе базы данных!")