from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import sqlite3
import csv

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = 'backend/students.db'

class Student(BaseModel):
    student_id: str
    name: str
    birth_year: int
    major: str
    gpa: float


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    return conn


def init_db():
    conn = get_conn()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS students (
            student_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            birth_year INTEGER,
            major TEXT,
            gpa REAL
        )
    ''')
    conn.commit()
    conn.close()


init_db()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/students", response_model=List[Student])
def list_students():
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT student_id, name, birth_year, major, gpa FROM students")
    rows = c.fetchall()
    conn.close()
    return [Student(student_id=r[0], name=r[1], birth_year=r[2], major=r[3], gpa=r[4] or 0.0) for r in rows]

@app.post("/students", response_model=Student)
def add_student(student: Student):
    conn = get_conn()
    c = conn.cursor()
    try:
        c.execute("INSERT INTO students (student_id, name, birth_year, major, gpa) VALUES (?, ?, ?, ?, ?)",
                  (student.student_id, student.name, student.birth_year, student.major, student.gpa))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(status_code=400, detail="Student ID already exists")
    conn.close()
    return student

@app.put("/students/{student_id}", response_model=Student)
def edit_student(student_id: str, student: Student):
    conn = get_conn()
    c = conn.cursor()
    c.execute("UPDATE students SET name=?, birth_year=?, major=?, gpa=? WHERE student_id=?",
              (student.name, student.birth_year, student.major, student.gpa, student_id))
    if c.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Student not found")
    conn.commit()
    conn.close()
    return student

@app.delete("/students/{student_id}")
def delete_student(student_id: str):
    conn = get_conn()
    c = conn.cursor()
    c.execute("DELETE FROM students WHERE student_id=?", (student_id,))
    if c.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Student not found")
    conn.commit()
    conn.close()
    return {"detail": "Student deleted"}

@app.get("/export/csv")
def export_csv():
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT student_id, name, birth_year, major, gpa FROM students")
    rows = c.fetchall()
    conn.close()
    output_path = 'backend/students_export.csv'
    with open(output_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["student_id", "name", "birth_year", "major", "gpa"])
        writer.writerows(rows)
    return {"path": output_path}
