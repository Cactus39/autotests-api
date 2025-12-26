from clients.public_http_builder import get_public_http_client
from clients.api_client import APIClient
from httpx import Response
from clients.users.user_schema import CreateUserRequestSchema, CreateUserResponseSchema

class PublicUsersClient(APIClient):
    """
    Клиент для работы с /api/v1/users
    """
    def create_user_api(self, request : CreateUserRequestSchema) -> Response:
        """
        Метод выполняет аутентификацию пользователя.

        :param request: Словарь с email, password, lastName, firstName и middleName.
        :return: Ответ от сервера в виде объекта httpx.Response.
        """
        return self.post(url="/api/v1/users", json=request.model_dump(by_alias=True))

    def create_user(self, request: CreateUserRequestSchema) -> CreateUserResponseSchema:
        response = self.create_user_api(request)
        return CreateUserResponseSchema.model_validate_json(response.text)

def get_public_users_client():
    """
     Функция создаёт экземпляр PublicUsersClient с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию PublicUsersClient.
    """
    return PublicUsersClient(client=get_public_http_client())

