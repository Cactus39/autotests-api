import pytest
import allure

from allure_commons.types import Severity
from http import HTTPStatus
from fixtures.courses import CourseFixture
from fixtures.users import UserFixture
from fixtures.files import FileFixture
from clients.courses.courses_client import CoursesClient
from clients.courses.courses_schema import UpdateCourseResponseSchema, UpdateCourseRequestSchema, GetCoursesQuerySchema,\
    GetCoursesResponseSchema, CreateCourseRequestSchema, CreateCourseResponseSchema
from tools.assertions.schema import validate_json_schema
from tools.assertions.base import assert_status_code
from tools.assertions.courses import asser_update_course_response, assert_get_courses_response, assert_create_course_response
from tools.allure.tags import AllureTag
from tools.allure.epics import AllureEpic
from tools.allure.features import AllureFeature
from tools.allure.stories import AllureStory

@allure.epic(AllureEpic.LMS)
@allure.feature(AllureFeature.COURSES)
@allure.parent_suite(AllureEpic.LMS)
@allure.suite(AllureFeature.COURSES)
@pytest.mark.regression
@pytest.mark.courses
@allure.tag(AllureTag.REGRESSION, AllureTag.COURSES)
class TestCourses:
    @allure.story(AllureStory.UPDATE_ENTITY)
    @allure.sub_suite(AllureStory.UPDATE_ENTITY)
    @allure.tag(AllureTag.UPDATE_ENTITY)
    @allure.title("Update course")
    @allure.severity(Severity.CRITICAL)
    def test_update_course(self, function_course: CourseFixture, courses_client: CoursesClient):
        # Формируем данные для обновления
        request = UpdateCourseRequestSchema(title="MY_TITLE", min_score=None, max_score=None, estimated_time=None, description=None)
        # Отправляем запрос на обновление курса
        response = courses_client.update_course_api(function_course.response.course.id, request=request)

        # Проверяем статус-код ответа
        assert_status_code(response.status_code, HTTPStatus.OK)
        # Преобразуем JSON-ответ в объект схемы
        response_data = UpdateCourseResponseSchema.model_validate_json(response.text)
        # Проверяем, что данные в ответе соответствуют запросу
        asser_update_course_response(request, response_data)
        # Валидируем JSON-схему ответа
        validate_json_schema(response.json(), response_data.model_json_schema())

    @allure.story(AllureStory.GET_ENTITIES)
    @allure.sub_suite(AllureStory.GET_ENTITIES)
    @allure.tag(AllureTag.GET_ENTITIES)
    @allure.title("Get courses")
    @allure.severity(Severity.BLOCKER)
    def test_get_courses(self, function_course: CourseFixture, function_user: UserFixture, courses_client: CoursesClient):
        # Формируем параметры запроса, передавая user_id
        query = GetCoursesQuerySchema(user_id=function_user.response.user.id)
        # Отправляем GET-запрос на получение списка курсов
        response = courses_client.get_courses_api(query=query)
        # Проверяем, что код ответа 200 OK
        assert_status_code(response.status_code, HTTPStatus.OK)

        # Десериализуем JSON-ответ в Pydantic-модель
        response_data = GetCoursesResponseSchema.model_validate_json(response.text)
        # Проверяем, что список курсов соответствует ранее созданным курсам
        assert_get_courses_response(response_data, [function_course.response])
        # Проверяем соответствие JSON-ответа схеме
        validate_json_schema(response.json(), response_data.model_json_schema())

    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.sub_suite(AllureStory.CREATE_ENTITY)
    @allure.tag(AllureTag.CREATE_ENTITY)
    @allure.title("Create course")
    @allure.severity(Severity.BLOCKER)
    def test_create_course(self, function_user: UserFixture, function_file: FileFixture, courses_client: CoursesClient):
        # Формируем параметры запроса, передавая user_id и file_id
        request = CreateCourseRequestSchema(preview_file_id=function_file.response.file.id, created_by_user_id=function_user.response.user.id)
        # Отправляем запрос на создание курса
        response = courses_client.create_course_api(request=request)
        # Проверяем, что код ответа 200 OK
        assert_status_code(response.status_code, HTTPStatus.OK)

        # Десериализуем JSON-ответ в Pydantic-модель
        response_data = CreateCourseResponseSchema.model_validate_json(response.text)
        # Проверяем, что данные в ответе соответствуют запросу
        assert_create_course_response(request=request, response=response_data)
        # Проверяем соответствие JSON-ответа схеме
        validate_json_schema(response.json(), response_data.model_json_schema())

