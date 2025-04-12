from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from utils.base_model import Base

class DepartmentModel(Base):
    __tablename__ = 'departments'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)


class EmployeeModel(Base):
    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(20))
    description = Column(Text())
    department_id = Column(Integer, ForeignKey('departments.id'))
