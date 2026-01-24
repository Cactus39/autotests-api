import pytest
from clients.files.files_client import FilesClient
from clients.files.files_schema import CreateFileRequestSchema, CreateFileResponseSchema, GetFileResponseSchema
from tools.assertions.files import assert_create_file_response, assert_file_is_accessible, assert_get_file_response, \
    assert_create_file_with_empty_directory_response, assert_create_file_with_empty_filename_response, \
    assert_file_not_found_response, assert_get_file_with_incorrect_file_id_response
from tools.assertions.base import assert_status_code
from http import HTTPStatus
from tools.assertions.schema import validate_json_schema
from fixtures.files import FileFixture
from clients.errors_schema import ValidationErrorResponseSchema, InternalErrorResponseSchema

@pytest.mark.files
@pytest.mark.regression
class TestFiles:
    def test_create_file(self, files_client: FilesClient):
        request = CreateFileRequestSchema(upload_file='./testdata/test_file.png')
        response = files_client.create_file_api(request=request)

        assert_status_code(response.status_code, HTTPStatus.OK)
        response_data = CreateFileResponseSchema.model_validate_json(response.text)
        assert_create_file_response(request=request, response=response_data)

        validate_json_schema(response.json(), response_data.model_json_schema())

        assert_file_is_accessible(str(response_data.file.url))

    def test_get_file(self, files_client: FilesClient, function_file: FileFixture):

        file_id = function_file.response.file.id
        response = files_client.get_file_api(file_id=file_id)

        assert_status_code(response.status_code, HTTPStatus.OK)

        response_data = GetFileResponseSchema.model_validate_json(response.text)
        assert_get_file_response(response_data, function_file.response)

        validate_json_schema(response.json(), response_data.model_json_schema())


    def test_create_file_with_empty_filename(self, files_client: FilesClient):
        request = CreateFileRequestSchema(upload_file='./testdata/test_file.png', filename="")
        response = files_client.create_file_api(request)

        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)

        assert_create_file_with_empty_filename_response(response_data)

        validate_json_schema(response.json(), response_data.model_json_schema())

    def test_create_file_with_empty_directory(self, files_client: FilesClient):
        request = CreateFileRequestSchema(upload_file='./testdata/test_file.png', directory="")
        response = files_client.create_file_api(request)

        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)

        assert_create_file_with_empty_directory_response(response_data)

        validate_json_schema(response.json(), response_data.model_json_schema())

    def test_delete_file(self, files_client: FilesClient, function_file: FileFixture):
        file_id = function_file.response.file.id
        delete_response = files_client.delete_file_api(file_id)
        assert_status_code(delete_response.status_code, HTTPStatus.OK)

        get_response = files_client.get_file_api(file_id)
        assert_status_code(get_response.status_code, HTTPStatus.NOT_FOUND)

        get_response_data = InternalErrorResponseSchema.model_validate_json(get_response.text)
        assert_file_not_found_response(get_response_data)

        validate_json_schema(get_response.json(), get_response_data.model_json_schema())

    def test_get_file_with_incorrect_file_id(self, files_client: FilesClient):
        response = files_client.get_file_api("incorrect-file-id")
        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)

        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)
        assert_get_file_with_incorrect_file_id_response(response_data)

        validate_json_schema(response.json(), response_data.model_json_schema())