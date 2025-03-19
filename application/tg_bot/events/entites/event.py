from datetime import datetime
from pydantic import BaseModel, Field

class Event(BaseModel):

    id: int = Field(default=-1)
    name: str
    description: str
    date: datetime
