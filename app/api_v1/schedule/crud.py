from sqlalchemy import Row, RowMapping
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from typing import Optional, Type, TypeVar, Any, Sequence

from app.core.models import Course, Group, Lesson, Base

T = TypeVar("T", bound=Base)

class CRUDBase:
    def __init__(self, model: Type[T]):
        self.model = model

    async def get(self, db: AsyncSession, id: int) -> Optional[T]:
        result = await db.get(self.model, id)
        return result

    async def get_all(self, db: AsyncSession) -> Sequence[Row[Any] | RowMapping | Any]:
        result = await db.execute(select(self.model))
        return result.scalars().all()

    async def create(self, db: AsyncSession, obj_in: dict) -> Optional[T]:
        obj = self.model(**obj_in)
        db.add(obj)
        try:
            await db.commit()
        except IntegrityError as e:
            await db.rollback()
            print(f"IntegrityError: {e.orig}")
            return None
        await db.refresh(obj)
        return obj

    async def update(self, db: AsyncSession, db_obj: T, obj_in: dict) -> T:
        for key, value in obj_in.items():
            setattr(db_obj, key, value)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def delete(self, db: AsyncSession, id: int) -> Optional[T]:
        obj = await self.get(db, id)
        if obj:
            await db.delete(obj)
            await db.commit()
        return obj


course_crud = CRUDBase(Course)
group_crud = CRUDBase(Group)
lesson_crud = CRUDBase(Lesson)
