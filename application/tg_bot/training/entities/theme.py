from pydantic import BaseModel, Field

class Theme(BaseModel):

    id: int = Field(default=-1)
    name: str

