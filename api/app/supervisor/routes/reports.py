from typing import Optional

from fastapi import APIRouter, Query, HTTPException

from app.api.deps import SessionDep
from app.reports.service import ReportService
from app.reports.schemas import (
    DropoutDistributionResponse,
    FacultyDropoutDistributionResponse,
    DropoutFactorsImpactResponse,
)
from app.faculties import constants as faculty_reports
from app.faculties import crud as faculty_crud

router = APIRouter(prefix="/reports")


@router.get("/dropout-distribution", response_model=DropoutDistributionResponse)
async def get_dropout_distribution(
    db: SessionDep,
    faculty: Optional[faculty_reports.FacultiesOptions] = Query(
        None, description="Filter by faculty"
    ),
    model_version_id: int | None = Query(
        default=None, description="ID of the model version to use for predictions"
    ),
):
    """
    Get the distribution of dropout probabilities across all students
    """
    if faculty is not None:
        faculty_db = faculty_crud.get_faculty_by_short_name(db, faculty.value)
        if not faculty_db:
            raise HTTPException(
                status_code=404,
                detail="No se ha encontrado ninguna facultad con el nombre especificado.",
            )
        faculty_id = faculty_db.id
    else:
        faculty_id = None

    try:
        report_service = ReportService(db)
        return report_service.get_dropout_probability_distribution(
            faculty_id, model_version_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/faculty-dropout-distribution", response_model=FacultyDropoutDistributionResponse
)
async def get_faculty_dropout_distribution(
    db: SessionDep,
    faculty: Optional[faculty_reports.FacultiesOptions] = Query(
        None, description="Filter by faculty"
    ),
    model_version_id: int | None = Query(
        default=None, description="ID of the model version to use for predictions"
    ),
):
    """
    Get the distribution of dropout probabilities across all faculties
    """
    if faculty is not None:
        faculty_db = faculty_crud.get_faculty_by_short_name(db, faculty.value)
        if not faculty_db:
            raise HTTPException(
                status_code=404,
                detail="No se ha encontrado ninguna facultad con el nombre especificado.",
            )
        faculty_id = faculty_db.id
    else:
        faculty_id = None

    try:
        report_service = ReportService(db)
        return report_service.get_faculty_dropout_distribution(
            faculty_id, model_version_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/dropout-factors-impact", response_model=DropoutFactorsImpactResponse)
async def get_dropout_factors_impact(
    db: SessionDep,
    faculty: Optional[faculty_reports.FacultiesOptions] = Query(
        None, description="Filter by faculty"
    ),
    model_version_id: int | None = Query(
        default=None, description="ID of the model version to use for predictions"
    ),
):
    """
    Get the most impactful factors for student dropout
    """
    if faculty is not None:
        faculty_db = faculty_crud.get_faculty_by_short_name(db, faculty.value)
        if not faculty_db:
            raise HTTPException(
                status_code=404,
                detail="No se ha encontrado ninguna facultad con el nombre especificado.",
            )
        faculty_id = faculty_db.id
    else:
        faculty_id = None

    try:
        report_service = ReportService(db)
        return report_service.get_dropout_factors_impact(faculty_id, model_version_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
