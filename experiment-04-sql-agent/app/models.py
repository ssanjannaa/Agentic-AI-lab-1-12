"""
SQLAlchemy ORM Models — Company Analytics Domain
Experiment 04 — SQL Agent with Tool Use (MR23-1CS0436)
"""

from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    code = Column(String, nullable=False, unique=True)
    location = Column(String, nullable=False)
    budget = Column(Float, nullable=False)

    employees = relationship("Employee", back_populates="department")
    projects = relationship("Project", back_populates="department")

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    roll_code = Column(String, nullable=False, unique=True)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    job_title = Column(String, nullable=False)
    salary = Column(Float, nullable=False)
    hire_date = Column(String, nullable=False)

    department = relationship("Department", back_populates="employees")
    project_allocations = relationship("EmployeeProject", back_populates="employee")

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    budget = Column(Float, nullable=False)
    status = Column(String, nullable=False)

    department = relationship("Department", back_populates="projects")
    employee_allocations = relationship("EmployeeProject", back_populates="project")

class EmployeeProject(Base):
    __tablename__ = "employee_projects"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    hours_allocated = Column(Integer, nullable=False)

    employee = relationship("Employee", back_populates="project_allocations")
    project = relationship("Project", back_populates="employee_allocations")
