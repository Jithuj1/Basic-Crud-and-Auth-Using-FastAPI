from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Teacher(Base):
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    subject = Column(String)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    students = relationship("Student", back_populates="teacher")


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    s_class = Column(Integer)
    teacher_id = Column(Integer, ForeignKey('teachers.id'))
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    teacher = relationship("Teacher", back_populates="students")



