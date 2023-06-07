from sqlalchemy.orm import Session
from passlib.context import CryptContext
import models
import schemas
from passlib.hash import bcrypt



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_student(db: Session, student: schemas.TeacherCreate):
    hashed_password = pwd_context.hash(student.password)
    print(hashed_password)
    db_student = models.Student(name=student.name, s_class=student.s_class, username=student.username, hashed_password=hashed_password)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

def check_username(db:Session, username:str):
    return db.query(models.Student).filter(models.Student.username == username).first()

def get_all_student(db: Session, skip: int = 0, limit: int = 25):
    return db.query(models.Student).offset(skip).limit(limit).all()

def get_student(db: Session, student_id : int):
    return db.query(models.Student).filter(models.Student.id == student_id).first()

def assign(db: Session, data: schemas.AssignRole):
    print(data.student_id, data.teacher_id)
    std = get_student(db, student_id = data.student_id)
    if not std:
        return None
    std.teacher_id = data.teacher_id
    db.commit()
    db.refresh(std)
    return std

def check_user(db: Session, data : schemas.StudentCreate):
    user = check_username(db, username= data.username)
    if user and bcrypt.verify(data.password, user.hashed_password):
        return True
    return False