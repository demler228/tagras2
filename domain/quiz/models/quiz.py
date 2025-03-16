from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base
from pydantic import BaseModel

class Theme(Base):
    __tablename__ = "themes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    theme_name = Column(String, nullable=False)
    questions = relationship("Question", back_populates="theme")

class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    theme_id = Column(Integer, ForeignKey("themes.id"), nullable=False)
    question_text = Column(String, nullable=False)
    theme = relationship("Theme", back_populates="questions")
    answers = relationship("Answer", back_populates="question")

class Answer(Base):
    __tablename__ = "answers"
    id = Column(Integer, primary_key=True, autoincrement=True)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    answer_text = Column(String, nullable=False)
    is_correct = Column(Boolean, nullable=False)
    question = relationship("Question", back_populates="answers")

class QuizData(BaseModel):
    question: str
    answers: list[str]
    correct_answer: str

class ThemeCreate(BaseModel):
    theme_name: str

class QuizCreate(BaseModel):
    theme_name: str
    quiz_data: list[QuizData]