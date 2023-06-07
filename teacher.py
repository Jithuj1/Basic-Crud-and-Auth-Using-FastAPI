from sqlalchemy.orm import Session
from passlib.context import CryptContext
import models
import schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_teacher(db: Session, teacher: schemas.TeacherCreate):
    hashed_password = pwd_context.hash(teacher.password)
    print(hashed_password)
    db_teacher = models.Teacher(name=teacher.name, subject=teacher.subject,username=teacher.username, hashed_password=hashed_password)
    db.add(db_teacher)
    db.commit()
    db.refresh(db_teacher)
    return db_teacher


def get_teacher(db: Session, teacher_id : int):
    return db.query(models.Teacher).filter(models.Teacher.id == teacher_id).first()

def check_username(db:Session, username:str):
    return db.query(models.Teacher).filter(models.Teacher.username == username).first()

def get_all_teacher(db: Session, skip: int = 0, limit: int = 25):
    return db.query(models.Teacher).offset(skip).limit(limit).all()

def delete_teacher(db: Session, teacher_id : int):
    db_teacher = get_teacher(db, teacher_id=teacher_id)
    if db_teacher is None:
        return None
    db.delete(db_teacher)
    db.commit()
    return True
        
def update_teacher(db: Session, teacher_id: int, teacher_obj: schemas.TeacherCreate):
    db_teacher = get_teacher(db, teacher_id=teacher_id)
    if not db_teacher:
        return None
    print(teacher_obj)
    if teacher_obj.name:
        db_teacher.name = teacher_obj.name
    if teacher_obj.subject:
        db_teacher.subject = teacher_obj.subject
    if teacher_obj.username:
        db_teacher.username = teacher_obj.username
    db.commit()
    db.refresh(db_teacher)
    return db_teacher
    
