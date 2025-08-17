import csv
import io
from datetime import datetime
from typing import List, Dict, Any

import pandas as pd
import xlsxwriter
from sqlalchemy import select, desc, func
from sqlalchemy.orm import Session

from app.faculties import constants as faculty_constants
from app.faculties import crud as faculty_crud
from app.predictions.models import Prediction
from app.students import models, constants
from app.model_versions import crud as model_versions_crud


def get_students_for_export(
    db: Session,
    faculty: faculty_constants.FacultiesOptions | None = None,
    min_probability: int | None = None,
    max_probability: int | None = None,
    search: str | None = None,
    estado: constants.EstadoEnum = constants.EstadoEnum.VIGENTE,
    model_version_id: int | None = None,
    archived: bool = False,
) -> List[Dict[str, Any]]:
    """
    Get all students matching the filters for export purposes without pagination
    """
    # If model_version_id is provided, get the model version
    if model_version_id is not None:
        model_version = model_versions_crud.get_model_version(db, model_version_id)
        if model_version is None:
            # If model version not found, use the active model
            model_version = model_versions_crud.get_active_model_version(db)
    else:
        # If no model_version_id provided, use the active model
        model_version = model_versions_crud.get_active_model_version(db)

    # Get the model version string (e.g., "v1.0")
    model_version_str = f"v{model_version.version}.0" if model_version else None

    # First, create a subquery to get the latest prediction for each student
    latest_prediction_subq = select(
        Prediction.student_id,
        Prediction.dropout_probability,
        Prediction.model_version,
        Prediction.created_at,
        func.row_number()
        .over(partition_by=Prediction.student_id, order_by=desc(Prediction.created_at))
        .label("rn"),
    )

    # Filter by model version if specified
    if model_version_str:
        latest_prediction_subq = latest_prediction_subq.where(
            model_version_str == Prediction.model_version
        )

    latest_prediction_subq = latest_prediction_subq.subquery()

    # Filter to only get the most recent prediction for each student
    latest_prediction = (
        select(
            latest_prediction_subq.c.student_id,
            latest_prediction_subq.c.dropout_probability.label("latest_probability"),
            latest_prediction_subq.c.model_version.label("model_version"),
            latest_prediction_subq.c.created_at.label("prediction_date"),
        )
        .where(latest_prediction_subq.c.rn == 1)
        .subquery()
    )

    stmt = (
        select(
            models.Student,
            latest_prediction.c.latest_probability,
            latest_prediction.c.model_version,
            latest_prediction.c.prediction_date,
        )
        .filter(estado == models.Student.estado)
        .outerjoin(
            latest_prediction, models.Student.id == latest_prediction.c.student_id
        )
    )

    # Filter by faculty if specified
    if faculty:
        db_faculty = faculty_crud.get_faculty_by_short_name(db, name=faculty.value)
        if db_faculty:
            stmt = stmt.where(db_faculty.id == models.Student.faculty_id)

    if archived is True:
        stmt = stmt.where(True == models.Student.archived)

    # Filter by dropout probability range if specified
    if min_probability is not None:
        min_value = min_probability / 100.0  # Convert percentage to decimal
        # Only include students with predictions that meet the minimum threshold
        stmt = stmt.where(latest_prediction.c.latest_probability >= min_value)

    if max_probability is not None:
        max_value = max_probability / 100.0  # Convert percentage to decimal
        # Only include students with predictions that meet the maximum threshold
        stmt = stmt.where(latest_prediction.c.latest_probability <= max_value)

    # Filter by search term if specified
    if search:
        search_term = f"%{search}%"
        stmt = stmt.where(
            (models.Student.first_name.ilike(search_term))
            | (models.Student.last_name.ilike(search_term))
        )

    if min_probability is not None and max_probability is not None:
        # Order by dropout probability in descending order, placing NULL values last
        stmt = stmt.order_by(
            latest_prediction.c.latest_probability.is_(None).asc(),
            desc(latest_prediction.c.latest_probability),
        )
    else:
        stmt = stmt.filter(latest_prediction.c.latest_probability.is_(None))

    result = db.execute(stmt).all()

    # Process the results into a list of dictionaries
    students_data = []
    for row in result:
        student = row[0]  # The Student object
        dropout_probability = row[1]  # The latest_probability value
        model_version = row[2]  # The model_version value
        prediction_date = row[3]  # The prediction_date value

        # Get faculty name
        faculty_name = student.faculty.short_name if student.faculty else "N/A"
        faculty_long_name = student.faculty.long_name if student.faculty else "N/A"

        # Format the student data for export
        student_data = {
            "ID": student.id,
            "Nombre": student.first_name,
            "Apellido": student.last_name,
            "Facultad": faculty_name,
            "Nombre Facultad": faculty_name,
            "Predicción (%)": round((dropout_probability or 0) * 100, 2),
            "Versión del Modelo": model_version or "N/A",
            "Fecha de Predicción": prediction_date.strftime("%Y-%m-%d %H:%M:%S")
            if prediction_date
            else "N/A",
            "Estado Civil": student.estado_civil if student.estado_civil else "N/A",
            "Fecha de Nacimiento": student.fecha_nac.strftime("%Y-%m-%d")
            if student.fecha_nac
            else "N/A",
            "Número de Hijos": student.nro_hijos,
            "Año de Egreso": student.anio_egreso,
            "Promedio Secundaria": student.promedio_secundaria
            if student.promedio_secundaria
            else "N/A",
            "Colegios Secundaria": student.cuantos_colegios_secundaria,
            "Posee Enfermedad": student.posee_enfermedad
            if student.posee_enfermedad
            else "N/A",
            "Vive Con": student.vive_con if student.vive_con else "N/A",
            "Situación Ocupacional": student.situacion_ocupacional
            if student.situacion_ocupacional
            else "N/A",
            "Sustento Económico": student.sustento_economico
            if student.sustento_economico
            else "N/A",
            "Formación Académica Padre": student.formacion_academica_padre
            if student.formacion_academica_padre
            else "N/A",
            "Formación Académica Madre": student.formacion_academica_madre
            if student.formacion_academica_madre
            else "N/A",
            "Formación Académica Hermanos": student.formacion_academica_hermanos
            if student.formacion_academica_hermanos
            else "N/A",
            "Último semestre": student.ultimo_semestre_cursado,
            "Estado": student.estado,
        }

        students_data.append(student_data)

    return students_data


def export_students_to_csv(
    db: Session,
    faculty: faculty_constants.FacultiesOptions | None = None,
    min_probability: int | None = None,
    max_probability: int | None = None,
    search: str | None = None,
    estado: constants.EstadoEnum = constants.EstadoEnum.VIGENTE,
    model_version_id: int | None = None,
    archived: bool = False,
) -> bytes:
    """
    Export students data to CSV format
    """
    students_data = get_students_for_export(
        db,
        faculty,
        min_probability,
        max_probability,
        search,
        estado,
        model_version_id,
        archived,
    )

    if not students_data:
        return b"No data available for export"

    # Create a CSV in memory
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=students_data[0].keys())
    writer.writeheader()
    writer.writerows(students_data)

    return output.getvalue().encode(
        "utf-8-sig"
    )  # Use UTF-8 with BOM for Excel compatibility


def export_students_to_excel(
    db: Session,
    faculty: faculty_constants.FacultiesOptions | None = None,
    min_probability: int | None = None,
    max_probability: int | None = None,
    search: str | None = None,
    estado: constants.EstadoEnum = constants.EstadoEnum.VIGENTE,
    model_version_id: int | None = None,
    archived: bool = False,
) -> bytes:
    """
    Export students data to Excel format
    """
    students_data = get_students_for_export(
        db,
        faculty,
        min_probability,
        max_probability,
        search,
        estado,
        model_version_id,
        archived,
    )

    if not students_data:
        return b"No data available for export"

    # Create an Excel file in memory
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet("Estudiantes")

    # Add header formats
    header_format = workbook.add_format(
        {
            "bold": True,
            "bg_color": "#4B5563",
            "font_color": "white",
            "border": 1,
            "align": "center",
        }
    )

    # Add data formats
    data_format = workbook.add_format(
        {
            "border": 1,
        }
    )

    # Add probability format (with conditional formatting)
    probability_format_high = workbook.add_format(
        {
            "border": 1,
            "bg_color": "#FEE2E2",  # Light red
        }
    )

    probability_format_medium = workbook.add_format(
        {
            "border": 1,
            "bg_color": "#FEF3C7",  # Light yellow
        }
    )

    probability_format_low = workbook.add_format(
        {
            "border": 1,
            "bg_color": "#D1FAE5",  # Light green
        }
    )

    # Write headers
    headers = list(students_data[0].keys())
    for col, header in enumerate(headers):
        worksheet.write(0, col, header, header_format)

    # Write data
    probability_col_index = headers.index("Predicción (%)")

    for row, student in enumerate(students_data, start=1):
        for col, (key, value) in enumerate(student.items()):
            # Apply conditional formatting to probability column
            if col == probability_col_index:
                if value >= 70:
                    worksheet.write(row, col, value, probability_format_high)
                elif value >= 40:
                    worksheet.write(row, col, value, probability_format_medium)
                else:
                    worksheet.write(row, col, value, probability_format_low)
            else:
                worksheet.write(row, col, value, data_format)

    # Auto-adjust column widths
    for col, header in enumerate(headers):
        max_width = len(header) + 2
        for row in range(len(students_data)):
            cell_value = str(students_data[row][header])
            if len(cell_value) > max_width:
                max_width = len(cell_value)
        worksheet.set_column(col, col, max_width)

    # Add title and metadata
    title_format = workbook.add_format(
        {
            "bold": True,
            "font_size": 14,
        }
    )

    # Add a title row at the top
    faculty_name = faculty.value if faculty else "Todas las Facultades"
    probability_range = f"{min_probability or 0}% - {max_probability or 100}%"
    current_date = datetime.now().strftime("%Y-%m-%d")

    # Add a summary sheet
    summary_sheet = workbook.add_worksheet("Resumen")
    summary_sheet.write(
        0, 0, "Reporte de Estudiantes con Riesgo de Deserción", title_format
    )
    summary_sheet.write(2, 0, f"Facultad: {faculty_name}")
    summary_sheet.write(3, 0, f"Rango de Predicción: {probability_range}")
    summary_sheet.write(4, 0, f"Fecha de Generación: {current_date}")
    summary_sheet.write(5, 0, f"Total de Estudiantes: {len(students_data)}")

    # Add statistics if there are students
    if students_data:
        # Calculate statistics
        probabilities = [student["Predicción (%)"] for student in students_data]
        avg_probability = sum(probabilities) / len(probabilities)
        high_risk = sum(1 for p in probabilities if p >= 70)
        medium_risk = sum(1 for p in probabilities if 40 <= p < 70)
        low_risk = sum(1 for p in probabilities if p < 40)

        summary_sheet.write(7, 0, "Estadísticas:")
        summary_sheet.write(8, 0, f"Predicción Promedio: {avg_probability:.2f}%")
        summary_sheet.write(9, 0, f"Estudiantes de Alto Riesgo (≥70%): {high_risk}")
        summary_sheet.write(
            10, 0, f"Estudiantes de Riesgo Medio (40-69%): {medium_risk}"
        )
        summary_sheet.write(11, 0, f"Estudiantes de Bajo Riesgo (<40%): {low_risk}")

    workbook.close()

    # Get the Excel data
    excel_data = output.getvalue()
    output.close()

    return excel_data


def export_students_to_pdf(
    db: Session,
    faculty: faculty_constants.FacultiesOptions | None = None,
    min_probability: int | None = None,
    max_probability: int | None = None,
    search: str | None = None,
    estado: constants.EstadoEnum = constants.EstadoEnum.VIGENTE,
    model_version_id: int | None = None,
    archived: bool = False,
) -> bytes:
    """
    Export students data to PDF format
    """
    try:
        import matplotlib.pyplot as plt
        from matplotlib.backends.backend_pdf import PdfPages
    except ImportError:
        # If matplotlib is not available, return a message
        return b"PDF export requires matplotlib. Please install it with 'pip install matplotlib'"

    students_data = get_students_for_export(
        db,
        faculty,
        min_probability,
        max_probability,
        search,
        estado,
        model_version_id,
        archived,
    )

    if not students_data:
        return b"No data available for export"

    # Convert to DataFrame for easier manipulation
    df = pd.DataFrame(students_data)

    # Create a PDF in memory
    output = io.BytesIO()

    with PdfPages(output) as pdf:
        # Create a title page
        plt.figure(figsize=(8.5, 11))
        plt.axis("off")

        faculty_name = faculty.value if faculty else "Todas las facultades"
        probability_range = f"{min_probability or 0}% - {max_probability or 100}%"
        current_date = datetime.now().strftime("%Y-%m-%d")

        plt.text(
            0.5,
            0.9,
            "Reporte de Estudiantes con Riesgo de Deserción",
            ha="center",
            fontsize=16,
            fontweight="bold",
        )
        plt.text(0.5, 0.85, f"Facultad: {faculty_name}", ha="center")
        plt.text(0.5, 0.82, f"Rango de predicción: {probability_range}", ha="center")
        plt.text(0.5, 0.79, f"Fecha de generación: {current_date}", ha="center")
        plt.text(0.5, 0.76, f"Total de estudiantes: {len(students_data)}", ha="center")

        # Add statistics if there are students
        if not df.empty:
            probabilities = df["Predicción (%)"]
            avg_probability = probabilities.mean()
            high_risk = (probabilities >= 70).sum()
            medium_risk = ((probabilities >= 40) & (probabilities < 70)).sum()
            low_risk = (probabilities < 40).sum()

            plt.text(0.5, 0.7, "Estadísticas:", ha="center", fontweight="bold")
            plt.text(
                0.5, 0.67, f"Predicción promedio: {avg_probability:.2f}%", ha="center"
            )
            plt.text(
                0.5,
                0.64,
                f"Estudiantes de Alto Riesgo (≥70%): {high_risk}",
                ha="center",
            )
            plt.text(
                0.5,
                0.61,
                f"Estudiantes de Riesgo Medio (40-69%): {medium_risk}",
                ha="center",
            )
            plt.text(
                0.5, 0.58, f"Estudiantes de Bajo Riesgo (<40%): {low_risk}", ha="center"
            )

            # Add a simple chart
            plt.axes([0.2, 0.3, 0.6, 0.2])
            categories = ["Alto Riesgo", "Riesgo Medio", "Bajo Riesgo"]
            values = [high_risk, medium_risk, low_risk]
            colors = ["#FEE2E2", "#FEF3C7", "#D1FAE5"]

            plt.bar(categories, values, color=colors)
            plt.title("Distribución de estudiantes por nivel de riesgo")
            plt.tight_layout()

        pdf.savefig()
        plt.close()

        # Create data pages (30 students per page)
        chunk_size = 30
        for i in range(0, len(df), chunk_size):
            chunk = df.iloc[i : i + chunk_size]

            # Select only the most important columns for the report
            display_cols = [
                "ID",
                "Nombre",
                "Apellido",
                "Facultad",
                "Predicción (%)",
                "Último semestre",
            ]

            # Filter columns that exist in the DataFrame
            display_cols = [col for col in display_cols if col in chunk.columns]

            # Create a figure and table
            fig, ax = plt.subplots(figsize=(8.5, 11))
            ax.axis("off")

            # Add a title
            ax.text(
                0.5,
                0.98,
                f"Estudiantes con Riesgo de Deserción (Página {i // chunk_size + 1})",
                ha="center",
                fontsize=12,
                fontweight="bold",
                transform=ax.transAxes,
            )

            # Create the table
            table_data = chunk[display_cols].values
            col_labels = display_cols

            # Color rows based on risk level
            row_colors = []
            for _, row in chunk.iterrows():
                prob = row["Predicción (%)"]
                if prob >= 70:
                    row_colors.append("#FEE2E2")  # Light red
                elif prob >= 40:
                    row_colors.append("#FEF3C7")  # Light yellow
                else:
                    row_colors.append("#D1FAE5")  # Light green

            # Create the table
            table = ax.table(
                cellText=table_data,
                colLabels=col_labels,
                loc="center",
                cellLoc="center",
                colLoc="center",
                cellColours=[
                    [row_color] * len(display_cols) for row_color in row_colors
                ],
            )

            # Style the table
            table.auto_set_font_size(False)
            table.set_fontsize(8)
            table.scale(1, 1.5)

            # Add header style
            for j, col in enumerate(col_labels):
                cell = table[(0, j)]
                cell.set_text_props(fontweight="bold", color="white")
                cell.set_facecolor("#4B5563")

            pdf.savefig(fig)
            plt.close()

    # Get the PDF data
    pdf_data = output.getvalue()
    output.close()

    return pdf_data
