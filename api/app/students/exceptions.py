from fastapi import HTTPException, status


class StudentNotFound(HTTPException):
    def __init__(self, detail: str = "Student not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
