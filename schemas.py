from pydantic import BaseModel
from typing import Optional



class TeacherBase(BaseModel):
    name: str
    subject: str

class TeacherCreate(TeacherBase):
    username: str
    password: str

class TeacherRead(TeacherBase):
    id: int

    class Config:
        orm_mode = True

class TeacherUpdate(TeacherBase):
    username:str

class StudentBase(BaseModel):
    s_class :  Optional[int] = None
    name:  Optional[str] = None
    teacher_id : Optional[int] = None

class StudentCreate(StudentBase):
    username: str
    password: str

class StudentRead(StudentBase):
    id: int

    class Config:
        orm_mode = True

class AssignRole(BaseModel):
    teacher_id : int
    student_id : int

class DistanceSchema(BaseModel):
    longitude1 : float
    longitude2 : float
    latitude1 : float
    latitude2 : float