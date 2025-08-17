from sqlalchemy.orm import Session

from app.model_versions import crud, exceptions
from app.logger.setup import logger


async def train_model(db: Session):
    """
    Task to train a new model version
    """
    try:
        crud.train_new_model_version(db)
    except exceptions.ModelIsCurrentlyUnderTraining:
        logger.warning(
            "Actualmente se está entrenando un modelo. El entrenamiento automático se canceló."
        )
    except exceptions.NoNewStudentsDataAvailable:
        logger.warning(
            "No existen nuevos datos de estudiantes para entrenar el modelo. El entrenamiento automático se canceló."
        )
    except Exception as e:
        logger.error(f"Error entrenando un nuevo modelo: {str(e)}")
    finally:
        db.close()
