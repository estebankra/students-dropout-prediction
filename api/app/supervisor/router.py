from fastapi import APIRouter

from app.supervisor.routes.students import router as supervisor_students_router
from app.supervisor.routes.reports import router as supervisor_reports_router

router = APIRouter(prefix="/supervisor")

router.include_router(supervisor_students_router)
router.include_router(supervisor_reports_router)
