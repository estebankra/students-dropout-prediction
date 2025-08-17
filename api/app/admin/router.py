from fastapi import APIRouter

from app.admin.routes.users import router as admin_users_router
from app.admin.routes.faculties import router as admin_faculties_router
from app.admin.routes.model_versions import router as admin_model_versions_router
from app.admin.routes.dashboard import router as admin_dashboard_router

router = APIRouter(prefix="/admin")

router.include_router(admin_users_router)
router.include_router(admin_faculties_router)
router.include_router(admin_model_versions_router)
router.include_router(admin_dashboard_router)
