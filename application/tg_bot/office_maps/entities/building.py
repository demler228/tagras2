from pydantic import BaseModel, Field

class Building(BaseModel):

    id: int = Field(default=-1)
    name: str
    photo_path: str

