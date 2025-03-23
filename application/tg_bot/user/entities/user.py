from pydantic import BaseModel, Field


class User(BaseModel):
    id: int = Field(default=-1)
    telegram_id: int
    tg_username: str
    username: str
    phone: str
    role: str
