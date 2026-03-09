from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from fastapi.staticfiles import StaticFiles
import os

from .models import Student
from .database import engine, init_db

app = FastAPI(title="Student Management API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/students")
def list_students(q: str = None):
    with Session(engine) as session:
        stmt = select(Student)
        if q:
            stmt = stmt.where(Student.name.contains(q))
        students = session.exec(stmt).all()
        return students


@app.post("/students", status_code=201)
def create_student(student: Student):
    with Session(engine) as session:
        existing = session.get(Student, student.student_id)
        if existing:
            raise HTTPException(status_code=400, detail="student_id already exists")
        session.add(student)
        session.commit()
        session.refresh(student)
        return student


@app.get("/students/{student_id}")
def get_student(student_id: str):
    with Session(engine) as session:
        student = session.get(Student, student_id)
        if not student:
            raise HTTPException(404, "Student not found")
        return student


@app.put("/students/{student_id}")
def update_student(student_id: str, student_data: Student):
    with Session(engine) as session:
        student = session.get(Student, student_id)
        if not student:
            raise HTTPException(404, "Student not found")
        student.name = student_data.name
        student.birth_year = student_data.birth_year
        student.major = student_data.major
        student.gpa = student_data.gpa
        session.add(student)
        session.commit()
        session.refresh(student)
        return student


@app.delete("/students/{student_id}", status_code=204)
def delete_student(student_id: str):
    with Session(engine) as session:
        student = session.get(Student, student_id)
        if not student:
            raise HTTPException(404, "Student not found")
        session.delete(student)
        session.commit()
        return


@app.get("/export")
def export_csv():
    from fastapi.responses import PlainTextResponse
    with Session(engine) as session:
        students = session.exec(select(Student)).all()
        output = "student_id,name,birth_year,major,gpa\n"
        for s in students:
            output += f'{s.student_id},{s.name},{s.birth_year},{s.major},{s.gpa}\n'
        return PlainTextResponse(content=output, media_type="text/csv")


@app.get("/stats")
def stats():
    with Session(engine) as session:
        students = session.exec(select(Student)).all()
        total = len(students)
        avg_gpa = round(sum(s.gpa for s in students) / total, 2) if total else 0
        by_major = {}
        for s in students:
            by_major[s.major] = by_major.get(s.major, 0) + 1
        return {"total": total, "average_gpa": avg_gpa, "by_major": by_major}


# Serve frontend static files so `frontend/index.html` is available at '/'
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
FRONTEND_DIR = os.path.join(ROOT_DIR, 'frontend')
if os.path.isdir(FRONTEND_DIR):
    app.mount('/', StaticFiles(directory=FRONTEND_DIR, html=True), name='frontend')
else:
    # fallback: mount project root if `frontend/` missing
    app.mount('/', StaticFiles(directory=ROOT_DIR, html=True), name='frontend')
