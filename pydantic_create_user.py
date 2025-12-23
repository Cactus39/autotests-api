from pydantic import BaseModel, EmailStr, Field
from clients.users.public_users_client import get_public_users_client


class UpdateUserRequestSchema(BaseModel):
    """
    Описание структуры запроса на обновление пользователя.
    """
    email: EmailStr
    last_name: str = Field(alias="lastName")
    first_name: str = Field(alias="firstName")
    middle_name: str = Field(alias="middleName")

class CreateUserRequestSchema(UpdateUserRequestSchema):
    """
    Описание структуры запроса на создание пользователя.
    """
    password: str

class UserSchema(UpdateUserRequestSchema):
    """
    Описание структуры пользователя.
    """
    id: str

class UserResponseShema(BaseModel):
    """
    Описание структуры ответа создания, получения, обновления  пользователя.
    """
    user: UserSchema
