from sqlmodel import SQLModel, Field


class Student(SQLModel, table=True):
    student_id: str = Field(primary_key=True)
    name: str
    birth_year: int
    major: str
    gpa: float
