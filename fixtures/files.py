import pytest
from pydantic import BaseModel
from clients.files.files_schema import CreateFileRequestSchema, CreateFileResponseSchema
from clients.files.files_client import get_files_client, FilesClient
from fixtures.users import UserFixture

class FileFixture(BaseModel):
    request: CreateFileRequestSchema
    response: CreateFileResponseSchema

@pytest.fixture(scope="function")
def files_client(function_user: UserFixture) -> FilesClient:
    return get_files_client(user=function_user.authentication_user)

@pytest.fixture(scope="function")
def function_file(files_client: FilesClient) -> FileFixture:
    request = CreateFileRequestSchema(upload_file="./testdata/test_file.png")
    response = files_client.create_file(request=request)

    return FileFixture(request=request, response=response)


