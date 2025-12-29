from pydantic import BaseModel, EmailStr, Field, ConfigDict
from tools.fakers import fake

class UpdateUserRequestSchema(BaseModel):
    """
    Описание структуры запроса на обновление пользователя.
    """
    model_config = ConfigDict(populate_by_name=True)

    email: EmailStr | None = Field(default_factory=fake.email)
    last_name: str | None = Field(alias="lastName", default_factory=fake.last_name)
    first_name: str | None = Field(alias="firstName", default_factory=fake.first_name)
    middle_name: str | None = Field(alias="middleName", default_factory=fake.middle_name)

class CreateUserRequestSchema(BaseModel):
    """
    Описание структуры запроса на создание пользователя.
    """
    model_config = ConfigDict(populate_by_name=True)

    password: str = Field(default_factory=fake.password)
    email: EmailStr = Field(default_factory=fake.email)
    last_name: str = Field(alias="lastName", default_factory=fake.last_name)
    first_name: str = Field(alias="firstName", default_factory=fake.first_name)
    middle_name: str = Field(alias="middleName", default_factory=fake.middle_name)

class UserSchema(UpdateUserRequestSchema):
    """
    Описание структуры пользователя.
    """
    model_config = ConfigDict(populate_by_name=True)

    id: str

class CreateUserResponseSchema(BaseModel):
    """
    Описание структуры ответа создания пользователя.
    """
    model_config = ConfigDict(populate_by_name=True)

    user: UserSchema

class UpdateUserResponseShema(CreateUserResponseSchema):
    """
    Описание структуры ответа обновления пользователя.
    """
    model_config = ConfigDict(populate_by_name=True)

class GetUserResponseSchema(CreateUserResponseSchema):
    """
    Описание структуры ответа получения пользователя.
    """
    model_config = ConfigDict(populate_by_name=True)

