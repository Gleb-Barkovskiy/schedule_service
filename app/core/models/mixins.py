from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, declared_attr, relationship
from sqlalchemy.testing.schema import mapped_column


if TYPE_CHECKING:
    from .group import Group
    from .course import Course


class GroupRelationMixin:
    _group_id_nullable: bool = False
    _group_id_unique: bool = False
    _group_back_populates: str | None = None

    @declared_attr
    def group_id(cls) -> Mapped[int]:
        return mapped_column(
            ForeignKey("groups.id"),
            unique=cls._group_id_unique,
            nullable=cls._group_id_nullable,
        )

    @declared_attr
    def group(cls) -> Mapped["Group"]:
        return relationship(
            "Group",
            back_populates=cls._group_back_populates,
        )


class CourseRelationMixin:
    _course_id_nullable: bool = False
    _course_id_unique: bool = False
    _course_back_populates: str | None = None

    @declared_attr
    def course_id(cls) -> Mapped[int]:
        return mapped_column(
            ForeignKey("courses.id"),
            unique=cls._course_id_unique,
            nullable=cls._course_id_nullable,
        )

    @declared_attr
    def course(cls) -> Mapped["Course"]:
        return relationship(
            "Course",
            back_populates=cls._course_back_populates,
        )
