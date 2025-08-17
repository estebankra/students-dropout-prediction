from pydantic import BaseModel
from app.model_versions import schemas as model_version_schemas
from app.users import schemas as user_schemas


class AdminDashboard(BaseModel):
    active_model: model_version_schemas.ModelVersionRead
    user_stats: user_schemas.UserStats


class SystemHealth(BaseModel):
    cpu_usage: float
    memory_usage: float
    disk_usage: float
    api_status: str
    database_status: str
    last_backup: str | None = None
    uptime: float
