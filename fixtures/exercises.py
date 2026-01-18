import pytest
from pydantic import BaseModel
from clients.exercises.exercises_client import get_exercises_client, ExercisesClient
from clients.exercises.exercises_schema import CreateExerciseRequestSchema, CreateExerciseResponseSchema
from fixtures.users import UserFixture
from fixtures.courses import CourseFixture


class ExerciseFixture(BaseModel):
    request: CreateExerciseRequestSchema
    response: CreateExerciseResponseSchema

@pytest.fixture(scope="function")
def exercises_client(function_user: UserFixture) -> ExercisesClient:
    return get_exercises_client(user=function_user.authentication_user)

@pytest.fixture(scope="function")
def function_exercise(exercises_client: ExercisesClient, function_course: CourseFixture) -> ExerciseFixture:
    request = CreateExerciseRequestSchema(courseId=function_course.response.course.id)
    response = exercises_client.create_exercise(request=request)
    return ExerciseFixture(request=request, response=response)
