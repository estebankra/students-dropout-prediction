from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRoute
from fastapi.staticfiles import StaticFiles
from fastapi_pagination import add_pagination
from sqlalchemy.orm import configure_mappers
from starlette.responses import JSONResponse

from app.api.routes import api_router
from app.config import settings
from app.database import engine, Base
from app.seeder import seeder

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from app.model_versions import tasks as model_version_tasks
from app.api.deps import get_db

from app.logger.setup import logger

configure_mappers()
Base.metadata.create_all(bind=engine)


# Add weekly job to train a new model version
def schedule_jobs() -> AsyncIOScheduler:
    """Initialize and schedule jobs."""
    scheduler = AsyncIOScheduler(timezone="UTC")

    logger.info("Adding weekly job to train a new model version.")
    scheduler.add_job(
        model_version_tasks.train_model,
        trigger=IntervalTrigger(days=7),
        args=[next(get_db())],
        id="train_model_job",
    )
    scheduler.start()
    logger.info("Scheduler started successfully.")
    return scheduler


def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"


@asynccontextmanager
async def lifespan(_: FastAPI):
    seeder.seed_db()
    logger.info("Initialize scheduler")
    async_scheduler = schedule_jobs()
    yield
    logger.info("Shutdown scheduler")
    async_scheduler.shutdown()


app_configs = {
    "title": "API",
    "openapi_url": f"{settings.API_VERSION}/openapi.json",
    "generate_unique_id_function": custom_generate_unique_id,
    "lifespan": lifespan,
}

app = FastAPI(**app_configs)
add_pagination(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_VERSION)

# Serve files in public directory
app.mount("/public", StaticFiles(directory="public"), name="public")


@app.exception_handler(Exception)
async def global_exception_handler(exc: Exception):
    print(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"message": "An error occurred. Try again later"},
    )
