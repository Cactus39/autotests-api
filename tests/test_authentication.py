from http import HTTPStatus
from clients.authentication.authentication_client import AuthenticationClient
from clients.authentication.authentication_schema import LoginRequestSchema, LoginResponseSchema
from tests.conftest import UserFixture
from tools.assertions.base import assert_status_code
from tools.assertions.schema import validate_json_schema
from tools.assertions.authentication import assert_login_response
import pytest

@pytest.mark.regression
@pytest.mark.authentication
def test_login(function_user: UserFixture, authentication_client: AuthenticationClient):

    # Authenticating user

    request = LoginRequestSchema(email=function_user.email,
                                                password=function_user.password)
    response = authentication_client.login_api(request)

    # Testing response status code
    assert_status_code(response.status_code, HTTPStatus.OK)

    # Testing response of an authenticated user
    response_data = LoginResponseSchema.model_validate_json(response.text)
    assert_login_response(response_data)

    # Testing json schema for validation errors
    validate_json_schema(response.json(), response_data.model_json_schema())