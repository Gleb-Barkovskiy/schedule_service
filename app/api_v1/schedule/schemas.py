from pydantic import BaseModel
from typing import Optional

class CourseCreate(BaseModel):
    course_number: str

class CourseUpdate(BaseModel):
    course_number: Optional[str] = None

class GroupCreate(BaseModel):
    group_number: str
    course_id: int

class GroupUpdate(BaseModel):
    group_number: Optional[str] = None

class LessonCreate(BaseModel):
    weekday: str
    subject: str
    teacher: str
    time: str
    lecture_practice: str
    room: str
    remarks: str
    course_id: int
    group_id: int

class LessonUpdate(BaseModel):
    weekday: Optional[str] = None
    subject: Optional[str] = None
    teacher: Optional[str] = None
    time: Optional[str] = None
    lecture_practice: Optional[str] = None
    room: Optional[str] = None
    remarks: Optional[str] = None
