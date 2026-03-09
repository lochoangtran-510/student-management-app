import csv
from sqlmodel import Session
from app.database import engine, init_db
from app.models import Student


def seed():
    # ensure database tables exist before seeding
    init_db()
    with Session(engine) as session:
        try:
            with open("backend/seed_data.csv", "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if session.get(Student, row["student_id"]):
                        continue
                    s = Student(
                        student_id=row["student_id"],
                        name=row["name"],
                        birth_year=int(row["birth_year"]),
                        major=row["major"],
                        gpa=float(row["gpa"]),
                    )
                    session.add(s)
                session.commit()
            print("Seed complete")
        except FileNotFoundError:
            print("seed_data.csv not found")


if __name__ == "__main__":
    seed()
