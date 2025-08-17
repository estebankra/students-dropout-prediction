from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.seeder.faculties import seed_faculties
from app.seeder.model_versions import seed_model_versions
from app.seeder.users import seed_users
from app.seeder.students import seed_students
from app.users import models as user_models


def seed_development(db: Session):
    seed_faculties(db)
    seed_model_versions(db)
    seed_users(db)
    seed_students(db)


def seed_db():
    try:
        db = SessionLocal()

        # Check if database was already seeded
        if db.query(user_models.User).first():
            db.close()
            return

        seed_development(db)
        db.close()
    except Exception as ex:
        print(str(ex))
        raise ex
