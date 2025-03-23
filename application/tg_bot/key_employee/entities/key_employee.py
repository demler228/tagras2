from pydantic import BaseModel, Field
from typing import Optional

class KeyEmployee(BaseModel):
    id: Optional[int] = Field(default=None)  # Необязательное поле
    telegram_username: Optional[str] = Field(default=None)
    username: str
    description: str
    phone: str
    role: str