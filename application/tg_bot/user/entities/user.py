from pydantic import BaseModel, Field
from typing import Optional


class User(BaseModel):
    id: int = Field(default=-1)
    telegram_id: Optional[int] = None
    tg_username: str
    username: str
    phone: str
    role: str = Field(default="user")
