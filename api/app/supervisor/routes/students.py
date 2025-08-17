from fastapi import APIRouter, Query, HTTPException, Response
from fastapi_pagination import LimitOffsetPage
from datetime import datetime

from app.api.deps import SessionDep, SupervisorRequired
from app.students import schemas as student_schemas
from app.students import crud as student_crud
from app.students import constants as student_constants
from app.supervisor.reports import students as supervisor_student_reports
from app.students import dependencies as student_dependencies
from app.faculties import constants as faculty_constants

router = APIRouter(prefix="/students")


@router.get("", response_model=LimitOffsetPage[student_schemas.Student])
def get_students(
    _supervisor: SupervisorRequired,
    db: SessionDep,
    faculty: faculty_constants.FacultiesOptions | None = None,
    min_probability: int | None = Query(default=None, ge=0, le=100),
    max_probability: int | None = Query(default=None, ge=0, le=100),
    search: str | None = None,
    estado: student_constants.EstadoEnum = student_constants.EstadoEnum.VIGENTE,
    model_version_id: int | None = Query(
        default=None, description="ID of the model version to use for predictions"
    ),
    archived: bool = False,
):
    return student_crud.get_students(
        db,
        faculty=faculty,
        min_probability=min_probability,
        max_probability=max_probability,
        search=search,
        estado=estado,
        model_version_id=model_version_id,
        archived=archived,
    )


@router.put("/{student_id}", response_model=student_schemas.Student)
async def update_student(
    db: SessionDep,
    student: student_dependencies.StudentDep,
    data: student_schemas.CreateOrUpdateStudent,
):
    try:
        student = student_crud.update_student(db, student, data)
        return student
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.get("/export/csv")
async def export_students_to_csv(
    _supervisor: SupervisorRequired,
    db: SessionDep,
    faculty: faculty_constants.FacultiesOptions | None = None,
    min_probability: int | None = Query(default=None, ge=0, le=100),
    max_probability: int | None = Query(default=None, ge=0, le=100),
    search: str | None = None,
    estado: student_constants.EstadoEnum = student_constants.EstadoEnum.VIGENTE,
    model_version_id: int | None = Query(
        default=None, description="ID of the model version to use for predictions"
    ),
    archived: bool = False,
):
    """
    Export students data to CSV format
    """
    try:
        csv_data = supervisor_student_reports.export_students_to_csv(
            db,
            faculty=faculty,
            min_probability=min_probability,
            max_probability=max_probability,
            search=search,
            estado=estado,
            model_version_id=model_version_id,
            archived=archived,
        )

        # Generate filename
        faculty_name = faculty.value if faculty else "todas"
        probability_range = f"{min_probability or 0}-{max_probability or 100}"
        date_str = datetime.now().strftime("%Y%m%d")
        filename = f"estudiantes_{faculty_name}_prob_{probability_range}_{date_str}.csv"

        # Return CSV file
        return Response(
            content=csv_data,
            media_type="text/csv",
            headers={
                "Content-Disposition": f'attachment; filename="{filename}"',
                "Access-Control-Expose-Headers": "Content-Disposition",
            },
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error exporting to CSV: {str(e)}")


@router.get("/export/excel")
async def export_students_to_excel(
    _supervisor: SupervisorRequired,
    db: SessionDep,
    faculty: faculty_constants.FacultiesOptions | None = None,
    min_probability: int | None = Query(default=None, ge=0, le=100),
    max_probability: int | None = Query(default=None, ge=0, le=100),
    search: str | None = None,
    estado: student_constants.EstadoEnum = student_constants.EstadoEnum.VIGENTE,
    model_version_id: int | None = Query(
        default=None, description="ID of the model version to use for predictions"
    ),
    archived: bool = False,
):
    """
    Export students data to Excel format
    """
    try:
        excel_data = supervisor_student_reports.export_students_to_excel(
            db,
            faculty=faculty,
            min_probability=min_probability,
            max_probability=max_probability,
            search=search,
            estado=estado,
            model_version_id=model_version_id,
            archived=archived,
        )

        # Generate filename
        faculty_name = faculty.value if faculty else "todas"
        probability_range = f"{min_probability or 0}-{max_probability or 100}"
        date_str = datetime.now().strftime("%Y%m%d")
        filename = (
            f"estudiantes_{faculty_name}_prob_{probability_range}_{date_str}.xlsx"
        )

        # Return Excel file
        return Response(
            content=excel_data,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={
                "Content-Disposition": f'attachment; filename="{filename}"',
                "Access-Control-Expose-Headers": "Content-Disposition",
            },
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error exporting to Excel: {str(e)}"
        )


@router.get("/export/pdf")
async def export_students_to_pdf(
    _supervisor: SupervisorRequired,
    db: SessionDep,
    faculty: faculty_constants.FacultiesOptions | None = None,
    min_probability: int | None = Query(default=None, ge=0, le=100),
    max_probability: int | None = Query(default=None, ge=0, le=100),
    search: str | None = None,
    estado: student_constants.EstadoEnum = student_constants.EstadoEnum.VIGENTE,
    model_version_id: int | None = Query(
        default=None, description="ID of the model version to use for predictions"
    ),
    archived: bool = False,
):
    """
    Export students data to PDF format
    """
    try:
        pdf_data = supervisor_student_reports.export_students_to_pdf(
            db,
            faculty=faculty,
            min_probability=min_probability,
            max_probability=max_probability,
            search=search,
            estado=estado,
            model_version_id=model_version_id,
            archived=archived,
        )

        # Generate filename
        faculty_name = faculty.value if faculty else "todas"
        probability_range = f"{min_probability or 0}-{max_probability or 100}"
        date_str = datetime.now().strftime("%Y%m%d")
        filename = f"estudiantes_{faculty_name}_prob_{probability_range}_{date_str}.pdf"

        # Return PDF file
        return Response(
            content=pdf_data,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f'attachment; filename="{filename}"',
                "Access-Control-Expose-Headers": "Content-Disposition",
            },
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error exporting to PDF: {str(e)}")
