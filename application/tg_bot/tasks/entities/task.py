from pydantic import BaseModel, Field
from datetime import datetime

class Task(BaseModel):
    id: int = Field(default=-1)
    name: str
    description: str
    creation_date: datetime
    deadline: datetime