from http import HTTPStatus
import pytest
import allure

from allure_commons.types import Severity
from fixtures.users import UserFixture
from clients.authentication.authentication_client import AuthenticationClient
from clients.authentication.authentication_schema import LoginRequestSchema, LoginResponseSchema
from tools.assertions.base import assert_status_code
from tools.assertions.schema import validate_json_schema
from tools.assertions.authentication import assert_login_response
from tools.allure.tags import AllureTag
from tools.allure.epics import AllureEpic
from tools.allure.features import AllureFeature
from tools.allure.stories import AllureStory

@allure.epic(AllureEpic.LMS)
@allure.feature(AllureFeature.AUTHENTICATION)
@allure.parent_suite(AllureEpic.LMS)
@allure.suite(AllureFeature.AUTHENTICATION)
@pytest.mark.regression
@pytest.mark.authentication
@allure.tag(AllureTag.REGRESSION, AllureTag.AUTHENTICATION)
class TestAuthentication:
    @allure.story(AllureStory.LOGIN)
    @allure.sub_suite(AllureStory.LOGIN)
    @allure.title("Login with correct email and password")
    @allure.severity(Severity.BLOCKER)
    def test_login(self, function_user: UserFixture, authentication_client: AuthenticationClient):

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