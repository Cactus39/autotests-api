from pydantic import BaseModel, Field, ConfigDict, EmailStr
from tools.fakers import fake

class LoginRequestSchema(BaseModel):
    """
    Описание структуры запроса на аутентификацию.
    """
    email: str = Field(default_factory=fake.email)
    password: str = Field(default_factory=fake.password)

class RefreshRequestSchema(BaseModel):
    """
    Описание структуры запроса для обновления токена.
    """
    model_config = ConfigDict(populate_by_name=True)

    refresh_token: str = Field(alias="refreshToken", default_factory=fake.sentence)

class TokenSchema(BaseModel):
    """
    Описание структуры аутентификационных токенов.
    """
    model_config = ConfigDict(populate_by_name=True)

    token_type: str = Field(alias="tokenType")
    access_token: str = Field(alias="accessToken")
    refresh_token: str = Field(alias="refreshToken")

class LoginResponseSchema(BaseModel):
    token : TokenSchema
