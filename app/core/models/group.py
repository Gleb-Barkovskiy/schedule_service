from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from .mixins import CourseRelationMixin


class Group(CourseRelationMixin, Base):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(primary_key=True)
    group_number: Mapped[str] = mapped_column(String(5))

    course = relationship("Course", back_populates="groups")
    lessons = relationship("Lesson", back_populates="group")
