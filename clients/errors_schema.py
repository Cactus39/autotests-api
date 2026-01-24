from pydantic import BaseModel, Field, ConfigDict
from typing import Any

class ValidationErrorSchema(BaseModel):
    """
    Модель, описывающая структуру ошибки валидации API.
    """
    model_config = ConfigDict(populate_by_name=True)

    type: str
    location: list[str] = Field(alias="loc")
    message: str = Field(alias="msg")
    input: Any
    context: dict[str, Any] = Field(alias="ctx")

class ValidationErrorResponseSchema(BaseModel):
    """
    Модель, описывающая структуру ответа API с ошибкой валидации.
    """

    details: list[ValidationErrorSchema] = Field(alias="detail")
    model_config = ConfigDict(populate_by_name=True)


class InternalErrorResponseSchema(BaseModel):
    """
    Модель для описания внутренней ошибки.
    """
    model_config = ConfigDict(populate_by_name=True)

    details: str = Field(alias="detail")

