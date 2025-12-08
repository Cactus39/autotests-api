from httpx import Client
from typing import TypedDict
from clients.authentication.authentication_client import get_authentication_client, LoginRequestDict

class AuthenticationUserDict(TypedDict):
    email: str
    password: str

def get_private_http_client(user: AuthenticationUserDict) -> Client:
    """
    Функция создаёт экземпляр httpx.Client с аутентификацией пользователя.

    :param user: Объект AuthenticationUserSchema с email и паролем пользователя.
    :return: Готовый к использованию объект httpx.Client с установленным заголовком Authorization.
    """
    auth_client = get_authentication_client()
    login_request = LoginRequestDict(email=user['email'],
                                     password=user['password'])
    login_response = auth_client.login(login_request)

    access_token = login_response['token']['accessToken']

    return Client(base_url="http://localhost:8000",
                  headers={"Authorization": f"Bearer {access_token}"},
                  timeout=100
                  )
