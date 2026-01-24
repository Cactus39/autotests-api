from tools.assertions.base import assert_equal, assert_length
from clients.errors_schema import ValidationErrorResponseSchema, ValidationErrorSchema, InternalErrorResponseSchema


def assert_validation_error(actual: ValidationErrorSchema, expected: ValidationErrorSchema):
    """
    Проверяет, что объект ошибки валидации соответствует ожидаемому значению.

    :param actual: Фактическая ошибка.
    :param expected: Ожидаемая ошибка.
    :raises AssertionError: Если значения полей не совпадают.
    """

    assert_equal(actual.type, expected.type, "type")
    assert_equal(actual.location, expected.location, "location")
    assert_equal(actual.message, expected.message, "message")
    assert_equal(actual.input, expected.input, "input")
    assert_equal(actual.context, expected.context, "context")


def assert_validation_error_response(actual: ValidationErrorResponseSchema, expected: ValidationErrorResponseSchema):
    """
    Проверяет, что объект ответа API с ошибками валидации (`ValidationErrorResponseSchema`)
    соответствует ожидаемому значению.

    :param actual: Фактический ответ API.
    :param expected: Ожидаемый ответ API.
    :raises AssertionError: Если значения полей не совпадают.
    """
    assert_length(actual.details, expected.details, "details")
    for actual_detail, expected_detail in zip(actual.details, expected.details):
        assert_validation_error(actual_detail, expected_detail)


def assert_internal_error_response(actual: InternalErrorResponseSchema, expected: InternalErrorResponseSchema):
    """
    Функция для проверки внутренней ошибки. Например, ошибки 404 (File not found).

    :param actual: Фактический ответ API.
    :param expected: Ожидаемый ответ API.
    :raises AssertionError: Если значения полей не совпадают.
    """
    assert_equal(actual.details, expected.details, "details")

