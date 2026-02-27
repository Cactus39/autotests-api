import pytest
from http import HTTPStatus

from clients.errors_schema import ValidationErrorSchema, InternalErrorResponseSchema
from clients.exercises.exercises_schema import CreateExerciseRequestSchema, CreateExerciseResponseSchema, \
    GetExerciseResponseSchema, UpdateExerciseRequestSchema, UpdateExerciseResponseSchema, GetExercisesQuerySchema, \
    GetExercisesResponseSchema
from clients.exercises.exercises_client import ExercisesClient
from fixtures.courses import CourseFixture
from fixtures.exercises import ExerciseFixture
from tools.assertions.exercises import assert_create_exercise_response, assert_get_exercise_response, \
    assert_update_exercise_response, assert_exercise_not_found_response, assert_get_exercises_response
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

    def test_update_exercise(self, function_exercise: ExerciseFixture, exercises_client: ExercisesClient):
        # Формируем параметры запроса
        exercise_id = function_exercise.response.exercise.id
        update_request = UpdateExerciseRequestSchema()
        # Отправляем запрос на обновление задания
        response = exercises_client.update_exercise_api(exercise_id=exercise_id, request=update_request)
        # Проверяем статус-код ответа
        assert_status_code(response.status_code, HTTPStatus.OK)

        # Преобразуем JSON-ответ в объект схемы
        response_data = UpdateExerciseResponseSchema.model_validate_json(response.text)
        # Проверяем, что данные в ответе соответствуют запросу
        assert_update_exercise_response(response_data, update_request)
        # Валидируем JSON-схему ответа
        validate_json_schema(response.json(), response_data.model_json_schema())

    def test_delete_exercise(self, function_exercise: ExerciseFixture, exercises_client: ExercisesClient):
        exercise_id = function_exercise.response.exercise.id
        # Удаляем задание
        delete_response = exercises_client.delete_exercise_api(exercise_id=exercise_id)
        # Проверяем, что задание успешно удалено (статус 200 OK)
        assert_status_code(delete_response.status_code, HTTPStatus.OK)

        # Пытаемся получить удаленное задание
        get_response = exercises_client.get_exercise_api(exercise_id=exercise_id)
        # Проверяем, что сервер вернул 404 Not Found
        assert_status_code(get_response.status_code, HTTPStatus.NOT_FOUND)

        # Проверяем, что в ответе содержится ошибка "Exercise not found"
        response_data = InternalErrorResponseSchema.model_validate_json(get_response.text)
        assert_exercise_not_found_response(response_data)

        # Проверяем, что ответ соответствует схеме
        validate_json_schema(get_response.json(), response_data.model_json_schema())

    def test_get_exercises(self, function_exercise: ExerciseFixture, exercises_client: ExercisesClient, function_course: CourseFixture):
        # Формируем параметры запроса, передавая course_id
        query = GetExercisesQuerySchema(course_id=function_course.response.course.id)
        # Отправляем GET-запрос на получение списка заданий
        response = exercises_client.get_exercises_api(query=query)
        # Проверяем, что код ответа 200 OK
        assert_status_code(response.status_code, HTTPStatus.OK)

        # Десериализуем JSON-ответ в Pydantic-модель
        response_data = GetExercisesResponseSchema.model_validate_json(response.text)
        # Проверяем, что список заданий соответствует ранее созданным заданиям
        assert_get_exercises_response(response_data, [function_exercise.response])
        # Проверяем соответствие JSON-ответа схеме
        validate_json_schema(response.json(), response_data.model_json_schema())

