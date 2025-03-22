from pydantic import BaseModel, Field


class UserTask(BaseModel):
    user_id: int = Field(default=-1)
    task_id: int = Field(default=-1)
