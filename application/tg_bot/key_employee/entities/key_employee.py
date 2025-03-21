from pydantic import BaseModel, Field

class KeyEmployee(BaseModel):
    id: int = Field(default=-1)
    telegram_id: int
    username: str
    description: str
    phone: str
    role: str