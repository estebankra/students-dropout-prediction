from pydantic import BaseModel


class FacultyBase(BaseModel):
    long_name: str
    short_name: str = None


class FacultyCreate(FacultyBase):
    pass


class FacultyUpdate(FacultyBase):
    active: bool


class FacultyRead(FacultyBase):
    id: int
    active: bool
