from fastapi import FastAPI, status, HTTPException
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
@app.get("/students", status_code=status.HTTP_200_OK)
def get_students():
    return {
        "success":True,
        "message": "Success",
        "data": students_db
    }

# POST: Add a student using the Body Model
@app.post("/students", status_code=status.HTTP_201_CREATED)
def create_student(student: Student):
    # .dict() or .model_dump() converts the object to a dictionary
    students_db.append(student.model_dump())
    return {
        "success":True,
        "message": "Success",
        "data": student
    }

# GET: Find one student
@app.get("/Students/{student_id}", status_code=status.HTTP_200_OK)
def get_student(student_id: int):
    for s in students_db:
        if s["id"] == student_id:
            return {
                "success":True,
                "message": "Success",
                "data": s
            }
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Student not found",
    )

# DELETE: Remove a student
@app.delete("/students/{student_id}", status_code=status.HTTP_200_OK)
def delete_student(student_id: int):
    for s in students_db:
        if s["id"] == student_id:
            students_db.remove(s)
            return {
                "success":True,
                "message": "Success",
                "data": f"Student {student_id} deleted"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Student not found",
    )