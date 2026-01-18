import pytest
from pydantic import BaseModel

from clients.courses.courses_schema import CreateCourseResponseSchema, CreateCourseRequestSchema
from clients.courses.courses_client import CoursesClient, get_courses_client
from fixtures.users import UserFixture
from fixtures.files import FileFixture

class CourseFixture(BaseModel):
    request: CreateCourseRequestSchema
    response: CreateCourseResponseSchema

@pytest.fixture(scope="function")
def courses_client(function_user: UserFixture) -> CoursesClient:
    return get_courses_client(function_user.authentication_user)

@pytest.fixture(scope="function")
def function_course(courses_client: CoursesClient,
                    function_user: UserFixture,
                    function_file: FileFixture) -> CourseFixture:

    request = CreateCourseRequestSchema(createdByUserId=function_user.response.user.id,
                                        previewFileId=function_file.response.file.id)
    response = courses_client.create_course(request=request)
    return CourseFixture(request=request, response=response)
