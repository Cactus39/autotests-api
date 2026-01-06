from http import HTTPStatus
from clients.users.public_users_client import get_public_users_client
from clients.users.user_schema import CreateUserRequestSchema
from clients.authentication.authentication_client import get_authentication_client
from clients.authentication.authentication_schema import LoginRequestSchema, LoginResponseSchema
from tools.assertions.base import assert_status_code
from tools.assertions.schema import validate_json_schema
from tools.assertions.authentication import assert_login_response
import pytest

@pytest.mark.regression
@pytest.mark.authentication
def test_login():
    # Creating user
    public_client = get_public_users_client()
    request_create_user = CreateUserRequestSchema()
    public_client.create_user(request_create_user)

    # Authenticating user
    authentication_client = get_authentication_client()
    authentication_payload = LoginRequestSchema(email=request_create_user.email,
                                                password=request_create_user.password)
    response = authentication_client.login_api(authentication_payload)

    # Testing response status code
    assert_status_code(response.status_code, HTTPStatus.OK)

    # Testing response of an authenticated user
    response_data = LoginResponseSchema.model_validate_json(response.text)
    assert_login_response(response_data)

    # Testing json schema for validation errors
    validate_json_schema(response.json(), response_data.model_json_schema())