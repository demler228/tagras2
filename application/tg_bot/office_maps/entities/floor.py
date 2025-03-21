from pydantic import BaseModel, Field

class Floor(BaseModel):

    id: int = Field(default=-1)
    name: str
    photo_path: str
    building_id: int

