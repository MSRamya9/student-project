# Import SQLite to connect Python with the database
import sqlite3

# FastAPI is used to create API endpoints
from fastapi import FastAPI, HTTPException

# BaseModel validates incoming JSON data
from pydantic import BaseModel


# Name of the SQLite database file
DATABASE_NAME = "student_info.db"

# Name of the SQL file containing the table and starting data
#SQL_FILE = "student_info.sql"


# Create the FastAPI application
app = FastAPI(
    title="Student Information API",
    description="API for managing student information",
    version="1.0"
)


# Defines the JSON structure required when creating a student
class Student(BaseModel):
    student_id: int
    first_name: str
    last_name: str
    phone_number: str | None = None
    address: str | None = None
    class_time: str | None = None


# Opens and returns a connection to the SQLite database
def get_database_connection():
    connection = sqlite3.connect(DATABASE_NAME)

    # Allows us to access columns by name
    connection.row_factory = sqlite3.Row

    return connection


# Creates the database and runs student_info.sql
def initialize_database():
    # Connect to the SQLite database
    connection = get_database_connection()

    # Create the table only when it does not already exist
    connection.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id INTEGER PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            phone_number TEXT,
            address TEXT,
            class_time TEXT
        )
    """)

    # Insert starting records only if their IDs do not already exist
    connection.executemany("""
        INSERT OR IGNORE INTO students (
            student_id,
            first_name,
            last_name,
            phone_number,
            address,
            class_time
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, [
        (
            1,
            "Ramya",
            "Mamillapalli",
            "404-555-0101",
            "Atlanta, GA",
            "09:00 AM"
        ),
        (
            2,
            "John",
            "Smith",
            "678-555-0102",
            "Marietta, GA",
            "10:30 AM"
        )
    ])

    # Save the changes and close the connection
    connection.commit()
    connection.close()


# Initialize the database when the application starts
initialize_database()


# Basic endpoint used to check whether the API is working
@app.get("/")
def home():
    return {"message": "Student Information API is running"}


# GET API: retrieve all students
@app.get("/students")
def get_all_students():
    connection = get_database_connection()

    students = connection.execute(
        "SELECT * FROM students"
    ).fetchall()

    connection.close()

    # Convert database rows into dictionaries for JSON output
    return [dict(student) for student in students]


# GET API: retrieve one student using student_id
@app.get("/students/{student_id}")
def get_student(student_id: int):
    connection = get_database_connection()

    student = connection.execute(
        "SELECT * FROM students WHERE student_id = ?",
        (student_id,)
    ).fetchone()

    connection.close()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return dict(student)


# POST API: add a new student
@app.post("/students", status_code=201)
def create_student(student: Student):
    connection = get_database_connection()

    try:
        connection.execute(
            """
            INSERT INTO students (
                student_id,
                first_name,
                last_name,
                phone_number,
                address,
                class_time
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                student.student_id,
                student.first_name,
                student.last_name,
                student.phone_number,
                student.address,
                student.class_time
            )
        )

        connection.commit()

    except sqlite3.IntegrityError:
        connection.close()

        raise HTTPException(
            status_code=409,
            detail="Student ID already exists"
        )

    connection.close()

    return {
        "message": "Student created successfully",
        "student": student
    }


# DELETE API: delete a student
@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    connection = get_database_connection()

    cursor = connection.execute(
        "DELETE FROM students WHERE student_id = ?",
        (student_id,)
    )

    connection.commit()
    connection.close()

    if cursor.rowcount == 0:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return {"message": "Student deleted successfully"}

# Connect to the database
connection = get_database_connection()

# Retrieve all student records
students = connection.execute(
    "SELECT * FROM students"
).fetchall()

# Display each student
for student in students:
    print(
        student["student_id"],
        student["first_name"],
        student["last_name"],
        student["phone_number"],
        student["address"],
        student["class_time"]
    )

# Close the connection
connection.close()