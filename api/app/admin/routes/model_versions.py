from fastapi import APIRouter, HTTPException, Query

from app.api.deps import SessionDep, AdminRequired
from app.model_versions import helpers, crud, exceptions

router = APIRouter(prefix="/models")


@router.post("/{model_id}/activate")
def activate_model(
    db: SessionDep,
    _admin: AdminRequired,
    model_id: int,
):
    """
    Endpoint to set a specific model as active.
    """
    try:
        # Get the model to activate
        model_to_activate = crud.get_model_version(db, model_id)
        if not model_to_activate:
            raise HTTPException(
                status_code=404,
                detail=f"No se ha encontrado ningún modelo con id #{model_id}",
            )

        # Check if the model is already active
        if model_to_activate.is_active:
            return {"message": "Este modelo ya está activo", "model_id": model_id}

        # Set the model as active
        crud.set_active_model_version(db, model_to_activate)

        return {
            "message": f"Modelo #{model_id} (versión v{model_to_activate.version}.0) activado con éxito",
            "model_id": model_id,
            "model_version": model_to_activate.version,
        }
    except HTTPException as ex:
        raise ex
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("")
async def train_model(db: SessionDep, _admin: AdminRequired):
    """
    Endpoint to train a new AI model.
    Processes the data, trains a logistic regression model and saves the trained model to a file.
    """
    try:
        new_model_version, metrics, improvement_message = crud.train_new_model_version(
            db
        )
        return {
            "message": f"Modelo entrenado con éxito! {improvement_message}",
            "accuracy": metrics["accuracy"],
            "model_version": new_model_version.version,
            "model_path": new_model_version.model_path,
        }
    except exceptions.ModelIsCurrentlyUnderTraining:
        raise HTTPException(
            status_code=400,
            detail="Actualmente se está entrenando un modelo. Vuelva a intentarlo más tarde",
        )
    except exceptions.NoNewStudentsDataAvailable:
        raise HTTPException(
            status_code=400,
            detail="No existen nuevos datos de estudiantes para entrenar el modelo",
        )
    except HTTPException as ex:
        raise ex
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/compare")
def compare_model_versions(
    db: SessionDep,
    _admin: AdminRequired,
    model1_id: str = Query(..., description="ID of the first model to compare"),
    model2_id: str = Query(..., description="ID of the second model to compare"),
):
    model1 = crud.get_model_version(db, model1_id)
    if not model1:
        raise HTTPException(
            status_code=404,
            detail=f"No se ha encontrado ningún modelo con id #{model1_id}",
        )

    model2 = crud.get_model_version(db, model2_id)
    if not model2:
        raise HTTPException(
            status_code=404,
            detail=f"No se ha encontrado ningún modelo con id #{model2_id}",
        )

    improved, comparison_results = helpers.compare_model_versions(model1, model2)
    return comparison_results
