from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# 1. Define the "Body Model"
# This tells FastAPI what to expect in the JSON body
class Student(BaseModel):
    id: int
    name: str
    course: str

# Our in-memory list
students_db = []

# GET: See all students
@app.get("/getStudents")
def get_students():
    return students_db

# POST: Add a student using the Body Model
@app.post("/createStudents")
def create_student(student: Student):
    # .dict() or .model_dump() converts the object to a dictionary
    students_db.append(student.model_dump())
    return {"message": "Student added successfully", "data": student}

# GET: Find one student
@app.get("/getStudent/{student_id}")
def get_student(student_id: int):
    for s in students_db:
        if s["id"] == student_id:
            return s
    return {"error": "Student not found"}

# DELETE: Remove a student
@app.delete("/deleteStudents/{student_id}")
def delete_student(student_id: int):
    for s in students_db:
        if s["id"] == student_id:
            students_db.remove(s)
            return {"message": f"Student {student_id} deleted"}
    return {"error": "Student not found"}