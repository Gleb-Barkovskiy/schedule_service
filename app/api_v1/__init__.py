from fastapi import APIRouter

from .schedule.views import router as schedule_router

router = APIRouter()
router.include_router(router=schedule_router, prefix="/schedule")