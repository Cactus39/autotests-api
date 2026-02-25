import pytest
from http import HTTPStatus
from tools.assertions.courses import asser_update_course_response, assert_get_courses_response, assert_create_course_response
from tools.assertions.base import assert_status_code
from tools.assertions.schema import validate_json_schema
from fixtures.courses import CourseFixture
from clients.courses.courses_client import CoursesClient
from clients.courses.courses_schema import UpdateCourseResponseSchema, UpdateCourseRequestSchema, GetCoursesQuerySchema,\
    GetCoursesResponseSchema, CreateCourseRequestSchema, CreateCourseResponseSchema
from fixtures.users import UserFixture
from fixtures.files import FileFixture

@pytest.mark.regression
@pytest.mark.courses
class TestCourses:
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
        validate_json_schema(response_data.model_json_schema, response.json())

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
        validate_json_schema(response_data.model_json_schema, response.json())

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
        validate_json_schema(response_data.model_json_schema, response.json())

