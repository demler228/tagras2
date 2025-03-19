from typing import Optional
from pydantic import BaseModel

class Question(BaseModel):
    id: int
    theme_id: int
    text: str
    answers: list[str]
    correct_answer: Optional[str]

