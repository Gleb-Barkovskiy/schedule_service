from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.models import Course, Group, Lesson
from app.core.models import db_helper

router = APIRouter()

@router.get("/courses")
async def get_courses(session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    async with session.begin():
        result = await session.execute(select(Course))
        courses = result.scalars().all()
        if not courses:
            raise HTTPException(status_code=404, detail="No courses found")
        return courses


@router.get("/courses/{course_id}/groups")
async def get_groups_by_course_id(course_id: int, session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    async with session.begin():
        result = await session.execute(select(Group).filter(Group.course_id == course_id))
        groups = result.scalars().all()
        if not groups:
            raise HTTPException(status_code=404, detail=f"No groups found for course_id {course_id}")
        return groups


@router.get("/courses/{course_id}/groups/{group_id}/schedule")
async def get_schedule_by_course_id_group_id_weekday(
    course_id: int,
    group_id: int,
    weekday: str = Query(None, min_length=1, max_length=15),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    async with session.begin():
        query = select(Lesson).filter(Lesson.course_id == course_id, Lesson.group_id == group_id)

        if weekday:
            query = query.filter(Lesson.weekday == weekday)

        result = await session.execute(query)
        lessons = result.scalars().all()

        if not lessons:
            raise HTTPException(status_code=404, detail=f"No schedule found for course_id {course_id}, group_id {group_id}, weekday {weekday if weekday else ''}")

        return lessons
