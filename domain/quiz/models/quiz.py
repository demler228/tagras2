from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from pydantic import BaseModel
from datetime import datetime
from sqlalchemy import DateTime
from domain.quiz.models.base import Base
from sqlalchemy.sql import func


class ThemeBase(Base):
    __tablename__ = "themes"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()


class QuestionBase(Base):
    __tablename__ = 'questions'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    theme_id: Mapped[int] = mapped_column(ForeignKey("themes.id"), nullable=False)
    text: Mapped[str] = mapped_column(String, nullable=False)

    answers: Mapped[list["AnswerBase"]] = relationship("AnswerBase", back_populates="question")


class AnswerBase(Base):
    __tablename__ = "answers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id"), nullable=False)
    text: Mapped[str] = mapped_column(String, nullable=False)
    is_correct: Mapped[bool] = mapped_column(Boolean, nullable=False)

    question: Mapped["QuestionBase"] = relationship("QuestionBase", back_populates="answers")


class QuizResult(Base):
    __tablename__ = "quiz_results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    theme_id: Mapped[int] = mapped_column(ForeignKey("themes.id"), nullable=False)
    score: Mapped[int] = mapped_column(Integer, nullable=False)
    completed_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    theme: Mapped["ThemeBase"] = relationship("ThemeBase")


class QuizData(BaseModel):
    question: str
    answers: list[str]
    correct_answer: str


class ThemeCreate(BaseModel):
    theme_name: str


class QuizCreate(BaseModel):
    theme_name: str
    quiz_data: list[QuizData]