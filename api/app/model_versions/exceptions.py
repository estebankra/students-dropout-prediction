from fastapi import HTTPException, status


class ModelIsCurrentlyUnderTraining(HTTPException):
    def __init__(
        self,
        detail: str = "A model is currently under training. Please try again later",
    ):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class NoNewStudentsDataAvailable(HTTPException):
    def __init__(
        self, detail: str = "No new data available to train a new model version"
    ):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
