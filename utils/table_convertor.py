from typing import Type, TypeVar
from pydantic import BaseModel
from utils.base_model import Base

T = TypeVar('T', bound=BaseModel)

# Utility function to convert SQLAlchemy objects to Pydantic models.
def to_entity(db_object: Base, pydantic_model: Type[T]) -> T:
    return pydantic_model(**db_object.__dict__)
