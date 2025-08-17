from sqlalchemy.orm import Session

from app.faculties import constants as faculty_constants
from app.faculties import models as faculty_models


def seed_faculties(db: Session):
    for faculty in faculty_constants.FACULTIES:
        db.add(faculty_models.Faculty(**faculty))
        db.commit()
