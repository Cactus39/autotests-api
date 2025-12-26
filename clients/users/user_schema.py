from pydantic import BaseModel, EmailStr, Field, ConfigDict

class UpdateUserRequestSchema(BaseModel):
    """
    Описание структуры запроса на обновление пользователя.
    """
    model_config = ConfigDict(populate_by_name=True)

    email: EmailStr | None
    last_name: str | None = Field(alias="lastName")
    first_name: str | None = Field(alias="firstName")
    middle_name: str | None = Field(alias="middleName")

class CreateUserRequestSchema(UpdateUserRequestSchema):
    """
    Описание структуры запроса на создание пользователя.
    """
    model_config = ConfigDict(populate_by_name=True)

    password: str

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

