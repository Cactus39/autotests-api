from httpx import Client
from pydantic import BaseModel, ConfigDict
from clients.authentication.authentication_client import get_authentication_client
from clients.authentication.authentication_schema import LoginRequestSchema
from functools import lru_cache

class AuthenticationUserSchema(BaseModel):
    model_config = ConfigDict(frozen=True)
    email: str
    password: str

@lru_cache(maxsize=None)
def get_private_http_client(user: AuthenticationUserSchema) -> Client:
    """
    Функция создаёт экземпляр httpx.Client с аутентификацией пользователя.

    :param user: Объект AuthenticationUserSchema с email и паролем пользователя.
    :return: Готовый к использованию объект httpx.Client с установленным заголовком Authorization.
    """
    auth_client = get_authentication_client()
    login_request = LoginRequestSchema(email=user.email, password=user.password)
    login_response = auth_client.login(login_request)
    access_token = login_response.token.access_token
    return Client(base_url="http://localhost:8000",
                  headers={"Authorization": f"Bearer {access_token}"},
                  timeout=100
                  )
