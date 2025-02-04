from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from .mixins import CourseRelationMixin, GroupRelationMixin


class Lesson(CourseRelationMixin, GroupRelationMixin, Base):
    __tablename__ = "lessons"

    id: Mapped[int] = mapped_column(primary_key=True)
    weekday: Mapped[str] = mapped_column()
    subject: Mapped[str] = mapped_column()
    teacher: Mapped[str | None] = mapped_column()
    time: Mapped[str | None] = mapped_column()
    lecture_practice: Mapped[str | None] = mapped_column()
    room: Mapped[str | None] = mapped_column()
    remarks: Mapped[str | None] = mapped_column()

    group = relationship("Group", back_populates="lessons")
    course = relationship("Course", back_populates=None)
