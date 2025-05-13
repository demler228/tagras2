from pydantic import BaseModel, Field
from typing import Optional


class User(BaseModel):
    id: int = Field(default=-1)
    telegram_id: Optional[int] = None
    tg_username: Optional[str] = None
    username: Optional[str] = None
    phone: Optional[str] = None
    role: str = Field(default="user")
