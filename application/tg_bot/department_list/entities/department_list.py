from pydantic import BaseModel
from typing import Optional

class Department(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None

class Employee(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    phone: Optional[str] = None
    description: Optional[str] = None
    department_id: Optional[int] = None