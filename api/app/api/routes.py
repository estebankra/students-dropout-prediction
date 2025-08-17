from fastapi import APIRouter

from app.admin import router as admin_router
from app.supervisor import router as supervisor_router
from app.predictions import router as prediction_router
from app.auth import router as auth_router
from app.users import router as user_router
from app.students import router as student_router
from app.model_versions import router as model_version_router
from app.faculties import router as faculties_router

api_router = APIRouter()
api_router.include_router(auth_router.router, tags=["Authentication"])
api_router.include_router(admin_router.router, tags=["Admin"])
api_router.include_router(supervisor_router.router, tags=["Supervisor"])
api_router.include_router(student_router.router, tags=["Students"])
api_router.include_router(prediction_router.router, tags=["Predictions"])
api_router.include_router(model_version_router.router, tags=["Model Versions"])
api_router.include_router(faculties_router.router, tags=["Faculties"])
api_router.include_router(user_router.router, tags=["Users"])
