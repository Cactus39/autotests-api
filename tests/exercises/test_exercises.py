import pytest
from http import HTTPStatus
from clients.exercises.exercises_schema import CreateExerciseRequestSchema, CreateExerciseResponseSchema, \
    GetExerciseResponseSchema
from clients.exercises.exercises_client import ExercisesClient
from fixtures.courses import CourseFixture
from fixtures.exercises import ExerciseFixture
from tools.assertions.exercises import assert_create_exercise_response, assert_get_exercise_response
from tools.assertions.base import assert_status_code
from tools.assertions.schema import validate_json_schema

@pytest.mark.regression
@pytest.mark.exercises
class TestExercises:
    def test_create_exercise(self, function_course: CourseFixture, exercises_client: ExercisesClient):

        # Формируем параметры запроса
        request = CreateExerciseRequestSchema(course_id=function_course.response.course.id)
        # Отправляем запрос на создание задания
        response = exercises_client.create_exercise_api(request=request)
        # Проверяем, что код ответа 200 OK
        assert_status_code(response.status_code, HTTPStatus.OK)

        # Десериализуем JSON-ответ в Pydantic-модель
        response_data = CreateExerciseResponseSchema.model_validate_json(response.text)
        # Проверяем, что данные в ответе соответствуют запросу
        assert_create_exercise_response(response_data, request)
        # Проверяем соответствие JSON-ответа схеме
        validate_json_schema(response.json(), response_data.model_json_schema())

    # @pytest.mark.current
    def test_get_exercise(self, function_exercise: ExerciseFixture, exercises_client: ExercisesClient):
        # Формируем параметры запроса
        exercise_id = function_exercise.response.exercise.id
        # Отправляем запрос на получение задания
        response = exercises_client.get_exercise_api(exercise_id=exercise_id)
        # Проверяем, что код ответа 200 OK
        assert_status_code(response.status_code, HTTPStatus.OK)

        # Десериализуем JSON-ответ в Pydantic-модель
        response_data = GetExerciseResponseSchema.model_validate_json(response.text)
        # Проверяем, что данные в ответе соответствуют запросу
        assert_get_exercise_response(response_data, function_exercise.response)
        # Проверяем соответствие JSON-ответа схеме
        validate_json_schema(response.json(), response_data.model_json_schema())