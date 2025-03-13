from pydantic import BaseModel, Field

class Faq(BaseModel):

    id: int = Field(default=-1)
    question: str
    answer: str

