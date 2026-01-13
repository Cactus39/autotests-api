import pytest
from pydantic import BaseModel
from clients.users.public_users_client import get_public_users_client, PublicUsersClient
from clients.users.user_schema import CreateUserRequestSchema, CreateUserResponseSchema
from clients.users.private_users_client import get_private_users_client, AuthenticationUserSchema, PrivateUsersClient


class UserFixture(BaseModel):
    request: CreateUserRequestSchema
    response: CreateUserResponseSchema

    @property
    def email(self):
        return self.request.email
    @property
    def password(self):
        return self.request.password
    @property
    def authentication_user(self):
        return AuthenticationUserSchema(email=self.request.email, password=self.request.password)

@pytest.fixture(scope="function")
def public_users_client() -> PublicUsersClient:
    # Создаем новый API клиент для работы с аутентификацией
    return get_public_users_client()

@pytest.fixture(scope="function")
def private_users_client(function_user: UserFixture) -> PrivateUsersClient:
    # Создаем новый API клиент для работы с users
    return get_private_users_client(user=function_user.authentication_user)

@pytest.fixture(scope="function")
def function_user(public_users_client: PublicUsersClient) -> UserFixture:
    request = CreateUserRequestSchema()
    response = public_users_client.create_user(request)
    return UserFixture(request=request, response=response)

