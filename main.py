from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
import models
import schemas
import teacher
import student
from database import engine, SessionLocal
import authentication
from starlette.applications import Starlette
from starlette.middleware.sessions import SessionMiddleware
import secrets
from math import sqrt



models.Base.metadata.create_all(bind=engine)

random_secret_key = secrets.token_hex(32)

app = FastAPI()

app.add_middleware(
    SessionMiddleware,
    secret_key=random_secret_key,
    max_age=1800
)

app.include_router(authentication.router)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def Home():
    return {"Welcome": "Hello World"}

#  Crud operation for teacher 

@app.post("/teachers/", response_model=schemas.TeacherRead)
async def Create_new_teacher(teacher_obj:schemas.TeacherCreate, db: Session = Depends(get_db)):
    name = teacher_obj.name
    subject = teacher_obj.subject
    username = teacher_obj.username
    password = teacher_obj.password
    if name == "" or subject == "" or username == "" or password == "":
        raise HTTPException(status_code=400, detail="Blank space not allowed")
    db_teacher = teacher.check_username(db, username =teacher_obj.username)
    if db_teacher:
        raise HTTPException(status_code=400, detail="Username already registered")
    return teacher.create_teacher(db=db, teacher = teacher_obj)


@app.get("/teachers/", response_model=list[schemas.TeacherRead])
async def list_all_teacher(skip: int = 0, limit: int = 25, db: Session = Depends(get_db)):
    all_teachers = teacher.get_all_teacher(db, skip=skip, limit=limit)
    return all_teachers


@app.get("/teachers/{teacher_id}", response_model=schemas.TeacherRead)
def read_teacher(teacher_id: int, db: Session = Depends(get_db)):
    db_teacher = teacher.get_teacher(db, teacher_id=teacher_id)
    if db_teacher is None:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return db_teacher


@app.delete("/teachers/{teacher_id}")
def delete_teacher(teacher_id: int, db: Session = Depends(get_db)):
    print('reached here')
    res = teacher.delete_teacher(db, teacher_id=teacher_id)
    if res :
        return {"message": "Object Deleted"}
    raise HTTPException(status_code=404, detail="Teacher not found")


@app.put("/teachers/{teacher_id}", response_model=schemas.TeacherRead)
def update_teacher_details(teacher_id: int, teacher_obj: schemas.TeacherUpdate, db: Session = Depends(get_db)):
    print('reached here')
    db_teacher = teacher.get_teacher(db, teacher_id=teacher_id)
    if db_teacher is None:
        raise HTTPException(status_code=404, detail="User not found")
    return teacher.update_teacher(db=db, teacher_id=teacher_id, teacher_obj=teacher_obj)



# For user operations 

@app.post("/students/", response_model=schemas.StudentRead)
async def Create_new_student(student_obj:schemas.StudentCreate, db: Session = Depends(get_db)):
    name = student_obj.name
    s_class = student_obj.s_class
    username = student_obj.username
    password = student_obj.password
    if name == "" or s_class == "" or username == "" or password == "":
        raise HTTPException(status_code=400, detail="Blank space not allowed")
    db_student = student.check_username(db, username =student_obj.username)
    if db_student:
        raise HTTPException(status_code=400, detail="Username already registered")
    return student.create_student(db=db, student = student_obj)


@app.get("/students/", response_model=list[schemas.StudentRead])
async def list_all_student(skip: int = 0, limit: int = 25, db: Session = Depends(get_db)):
    all_student = student.get_all_student(db, skip=skip, limit=limit)
    print(all_student)
    return all_student


# assinging a new teacher to student 

@app.post("/assign_teacher/", response_model= schemas.StudentRead)
async def assign(data : schemas.AssignRole, db: Session = Depends(get_db)):
    teacher_id = data.teacher_id
    student_id = data.student_id
    std_obj = student.get_student(db, student_id = student_id)
    teacher_obj = teacher.get_teacher(db, teacher_id = teacher_id)
    print('here it is')
    if not std_obj or not teacher_obj:
        raise HTTPException(status_code=404, detail="Object Not found")
    print(teacher_id, student_id)
    result = student.assign(db, data=data)
    return result
    

@app.post("/distance")
async def dis(data : schemas.DistanceSchema):
    dif_of_lon = data.longitude2 - data.longitude1
    dif_of_lat = data.latitude2 - data.latitude1
    distance = sqrt( dif_of_lon**2 + dif_of_lat**2 )
    return {"Distance between these two place": distance}
