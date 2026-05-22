from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel

app = FastAPI()

# 1. Define the "Body Model"
# This tells FastAPI what to expect in the JSON body
class Student(BaseModel):
    id: int
    name: str
    age: int
    course: str

class Output(BaseModel):
    success: bool
    message: str
    data: Student

# Our in-memory list
students_db = []


# GET: See all students
@app.get("/api/v1/students", status_code=status.HTTP_200_OK, response_model=list[Output])
def get_students(id: int | None = None,name: str | None = None,age: int | None = None,course: str | None = None,skip: int = 0, limit: int = 10):

    result = students_db

    if id is not None:
        result = [s for s in students_db if s["id"] == id]
    if name is not None:
        result = [s for s in students_db if s["name"] == name]
    if age is not None:
        result = [s for s in students_db if s["age"] == age]
    if course is not None:
        result = [s for s in students_db if s["course"] == course]

    result = result[skip : limit]

    if result == []:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="no students has been added"
        )
    else:
        return {
            "success": True,
            "message": "Success",
            "data": result
        }

# POST: Add a student using the Body Model
@app.post("/api/v1/students", status_code=status.HTTP_201_CREATED)
def create_student(student: Student):
    # .dict() or .model_dump() converts the object to a dictionary
    students_db.append(student.model_dump())
    return {
        "success":True,
        "message": "Success",
        "data": student
    }

# GET: Find one student
@app.get("/api/v1/students/{student_id}", status_code=status.HTTP_200_OK, response_model=Output)
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
@app.delete("/api/v1/students/{student_id}", status_code=status.HTTP_200_OK, response_model=Output)
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