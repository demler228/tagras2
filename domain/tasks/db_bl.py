from pydantic import BaseModel, Field

class Section(BaseModel):

    id: int = Field(default=-1)
    name: str
    photo_path: str
    floor_id: int