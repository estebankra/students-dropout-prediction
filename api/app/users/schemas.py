from pydantic import BaseModel, EmailStr, Field, field_validator, ValidationInfo

from app.users import constants as user_constants


class UserBase(BaseModel):
    email: EmailStr
    first_name: str = Field(min_length=2, max_length=200)
    last_name: str = Field(min_length=2, max_length=200)
    picture: str | None = None


class UserCreate(UserBase):
    role: user_constants.Roles
    password: str = Field(
        min_length=8,
        max_length=128,
        description="Password must be at least 8 characters long.",
    )
    confirm_password: str = Field(
        min_length=8,
        max_length=128,
        description="Confirm password must be at least 8 characters long.",
    )

    @field_validator("confirm_password", mode="after")
    @classmethod
    def check_passwords_match(cls, value: str, info: ValidationInfo) -> str:
        if value != info.data["password"]:
            raise ValueError("Passwords do not match")
        return value


class UserUpdate(UserBase):
    role: user_constants.Roles
    active: bool
    password: str | None = Field(
        default=None,
        min_length=8,
        max_length=128,
        description="Password must be at least 8 characters long.",
    )
    confirm_password: str | None = Field(
        default=None,
        min_length=8,
        max_length=128,
        description="Confirm password must be at least 8 characters long.",
    )

    @field_validator("password", mode="after")
    @classmethod
    def validate_password_consistency(
        cls, value: str | None, info: ValidationInfo
    ) -> str | None:
        confirm_password = info.data.get("confirm_password")

        # If confirm_password is provided, password must also be provided
        if value is None and confirm_password is not None:
            raise ValueError("Password is missing but confirm password is provided")

        return value

    @field_validator("confirm_password", mode="after")
    @classmethod
    def check_passwords_match(
        cls, value: str | None, info: ValidationInfo
    ) -> str | None:
        password = info.data.get("password")

        # If password is not provided, confirm_password should also be None
        if password is None:
            if value is not None:
                raise ValueError("Confirm password provided but password is missing")
            return value

        # If password is provided, confirm_password must match
        if value != password:
            raise ValueError("Passwords do not match")

        return value


class UserRead(UserBase):
    id: int
    active: bool
    role: user_constants.Roles


class UserStats(BaseModel):
    total_users: int
    total_supervisors: int
    total_active_supervisors: int
    total_admins: int
    total_active_admins: int
    new_users_last_30_days: int
