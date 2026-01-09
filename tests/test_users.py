from http import HTTPStatus

from clients.users.private_users_client import PrivateUsersClient
from tests.conftest import UserFixture
from tools.assertions.schema import validate_json_schema
from clients.users.public_users_client import PublicUsersClient
from clients.users.user_schema import CreateUserRequestSchema, CreateUserResponseSchema, GetUserResponseSchema, UserSchema
from tools.assertions.base import  assert_status_code
from tools.assertions.users import assert_create_user_response, assert_get_user_response
import pytest

@pytest.mark.regression
@pytest.mark.users
def test_create_user(public_users_client: PublicUsersClient):

    request = CreateUserRequestSchema()
    response = public_users_client.create_user_api(request)

    assert_status_code(response.status_code, HTTPStatus.OK)

    response_data = CreateUserResponseSchema.model_validate_json(response.text)
    assert_create_user_response(request, response_data)



    validate_json_schema(response.json(), response_data.model_json_schema())

@pytest.mark.users
@pytest.mark.regression
def test_get_user_me(private_users_client: PrivateUsersClient, function_user: UserFixture):

    get_user_response = private_users_client.get_user_me_api()

    # Тест проверяет статус-код ответа (200)
    assert_status_code(get_user_response.status_code, HTTPStatus.OK)

    # Тест проверяет корректность тела ответа (GetUserResponseSchema)
    get_user_response_data = GetUserResponseSchema.model_validate_json(get_user_response.text)
    create_user_response_data = function_user.response
    assert_get_user_response(get_user_response_data, create_user_response_data)

    # Тест выполняет валидацию JSON schema (GetUserResponseSchema)
    validate_json_schema(get_user_response.json(), get_user_response_data.model_json_schema())