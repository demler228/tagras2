from pydantic import BaseModel, Field

class Material(BaseModel):

    id: int = Field(default=-1)
    title: str
    url: str
    theme_id: int
