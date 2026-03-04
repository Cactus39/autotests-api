from http import HTTPStatus
import pytest
import allure

from allure_commons.types import Severity
from fixtures.users import UserFixture
from clients.users.private_users_client import PrivateUsersClient
from clients.users.public_users_client import PublicUsersClient
from clients.users.user_schema import CreateUserRequestSchema, CreateUserResponseSchema, GetUserResponseSchema
from tools.fakers import fake
from tools.assertions.base import  assert_status_code
from tools.assertions.users import assert_create_user_response, assert_get_user_response
from tools.assertions.schema import validate_json_schema
from tools.allure.tags import AllureTag
from tools.allure.epics import AllureEpic
from tools.allure.features import AllureFeature
from tools.allure.stories import AllureStory

@allure.epic(AllureEpic.LMS)
@allure.feature(AllureFeature.USERS)
@pytest.mark.regression
@pytest.mark.users
@allure.tag(AllureTag.USERS, AllureTag.REGRESSION)
@allure.parent_suite(AllureEpic.LMS)
@allure.suite(AllureFeature.USERS)
class TestUser:
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.sub_suite(AllureStory.CREATE_ENTITY)
    @pytest.mark.parametrize("domain",["mail.ru", "gmail.com", "example.com"])
    @allure.title("Create user")
    @allure.tag(AllureTag.CREATE_ENTITY)
    @allure.severity(Severity.BLOCKER)
    def test_create_user(self, public_users_client: PublicUsersClient, domain: str | None):
        request = CreateUserRequestSchema(email=fake.email(domain=domain))
        response = public_users_client.create_user_api(request)

        assert_status_code(response.status_code, HTTPStatus.OK)

        response_data = CreateUserResponseSchema.model_validate_json(response.text)
        assert_create_user_response(request, response_data)



        validate_json_schema(response.json(), response_data.model_json_schema())

    @allure.story(AllureStory.GET_ENTITY)
    @allure.sub_suite(AllureStory.GET_ENTITY)
    @allure.title("Get user me")
    @allure.tag(AllureTag.GET_ENTITY)
    @allure.severity(Severity.CRITICAL)
    def test_get_user_me(self, private_users_client: PrivateUsersClient, function_user: UserFixture):

        get_user_response = private_users_client.get_user_me_api()

        # Тест проверяет статус-код ответа (200)
        assert_status_code(get_user_response.status_code, HTTPStatus.OK)

        # Тест проверяет корректность тела ответа (GetUserResponseSchema)
        get_user_response_data = GetUserResponseSchema.model_validate_json(get_user_response.text)
        create_user_response_data = function_user.response
        assert_get_user_response(get_user_response_data, create_user_response_data)

        # Тест выполняет валидацию JSON schema (GetUserResponseSchema)
        validate_json_schema(get_user_response.json(), get_user_response_data.model_json_schema())
