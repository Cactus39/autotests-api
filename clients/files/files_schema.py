from pydantic import BaseModel, HttpUrl, Field
from tools.fakers import fake

class CreateFileRequestSchema(BaseModel):
    """
    Описание структуры запроса на создание файла.
    """
    filename: str = Field(default_factory=lambda :f"{fake.uuid4()}.png")
    directory: str = Field(default="test_dir")
    upload_file: str

class FileSchema(BaseModel):
    """
    Описание структуры файла.
    """
    id: str
    url: HttpUrl
    filename: str
    directory: str

class CreateFileResponseSchema(BaseModel):
    """
    Описание структуры ответа создания файла.
    """
    file: FileSchema
