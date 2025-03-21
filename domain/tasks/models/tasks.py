from datetime import datetime
from pydantic import BaseModel, Field

class Task(BaseModel):

    id: int = Field(default=-1)
    name: str
    description: str
    creation_date: datetime
    deadline: datetime
