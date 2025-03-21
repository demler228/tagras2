from pydantic import BaseModel, Field
from typing import Optional

class KeyEmployee(BaseModel):
    id: int = Field(default=-1)
    telegram_username: Optional[str] = Field(default=None)
    username: str
    description: str
    phone: str
    role: str