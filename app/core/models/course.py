from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base


class Course(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(primary_key=True)
    course_number: Mapped[str] = mapped_column(String(5))

    # Relationship with Group
    groups = relationship("Group", back_populates="course")
