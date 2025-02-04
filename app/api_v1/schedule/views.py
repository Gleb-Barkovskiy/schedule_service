from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.models import db_helper
from .crud import course_crud, group_crud, lesson_crud

router = APIRouter()


@router.get("/")
async def get_courses(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    courses = await course_crud.get_all(session)
    if not courses:
        raise HTTPException(status_code=404, detail="No courses found")
    return courses


@router.get("/{course_id}/")
async def get_groups_by_course_id(
    course_id: int, session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    groups = await group_crud.search(session, {"course_id": course_id})
    if not groups:
        raise HTTPException(
            status_code=404, detail=f"No groups found for course_id {course_id}"
        )
    return groups


@router.get("/{course_id}/{group_id}/")
async def get_schedule_by_course_id_group_id_weekday(
    course_id: int,
    group_id: int,
    weekday: str = Query(None, min_length=1, max_length=15),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    filters = {"course_id": course_id, "group_id": group_id}
    if weekday:
        filters["weekday"] = weekday

    lessons = await lesson_crud.search(session, filters)
    if not lessons:
        raise HTTPException(
            status_code=404,
            detail=f"No schedule found for course_id {course_id}, group_id {group_id}, weekday {weekday if weekday else ''}",
        )
    return lessons
