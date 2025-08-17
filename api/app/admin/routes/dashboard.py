from fastapi import APIRouter
import psutil
import os
import datetime
from sqlalchemy import text

from app.admin import schemas
from app.api.deps import SessionDep, AdminRequired
from app.model_versions import crud as model_version_crud
from app.users import crud as user_crud


router = APIRouter(prefix="/dashboard")


@router.get("/stats", response_model=schemas.AdminDashboard)
async def get_dashboard_stats(db: SessionDep, _admin: AdminRequired):
    """Get all dashboard statistics in a single call"""
    # Get active model
    active_model = model_version_crud.get_active_model_version(db)

    # User stats
    user_stats = user_crud.get_user_stats(db)

    return {"active_model": active_model, "user_stats": user_stats}


@router.get("/system-health", response_model=schemas.SystemHealth)
async def get_system_health(db: SessionDep, _admin: AdminRequired):
    """Get system health information"""
    # Get CPU usage
    cpu_usage = psutil.cpu_percent()

    # Get memory usage
    memory = psutil.virtual_memory()
    memory_usage = memory.percent

    # Get disk usage
    disk = psutil.disk_usage("/")
    disk_usage = disk.percent

    # Check database status
    db_status = "offline"
    try:
        # Execute a simple query to check if database is responsive
        db.execute(text("SELECT 1"))
        db_status = "online"
    except Exception:
        pass

    # Get system uptime
    boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
    uptime = (datetime.datetime.now() - boot_time).days

    # TODO Try to get last backup time
    last_backup = None
    backup_dir = os.environ.get("BACKUP_DIR", "/backups")
    if os.path.exists(backup_dir):
        try:
            # Get the most recent file in the backup directory
            files = [
                os.path.join(backup_dir, f)
                for f in os.listdir(backup_dir)
                if f.endswith(".backup")
            ]
            if files:
                last_backup = datetime.datetime.fromtimestamp(
                    max(os.path.getmtime(f) for f in files)
                ).isoformat()
        except Exception:
            pass

    return {
        "cpu_usage": cpu_usage,
        "memory_usage": memory_usage,
        "disk_usage": disk_usage,
        "api_status": "online",  # Since we're responding, API is online
        "database_status": db_status,
        "last_backup": last_backup,
        "uptime": uptime,
    }
