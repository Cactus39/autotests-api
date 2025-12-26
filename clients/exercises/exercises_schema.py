from pydantic import BaseModel, Field, ConfigDict

class GetExercisesQuerySchema(BaseModel):
    """
    Описание структуры запроса на получение списка заданий для определенного курса.
    """
    model_config = ConfigDict(populate_by_name=True)

    course_id: str = Field(alias="courseId")

class CreateExerciseRequestSchema(BaseModel):
    """
    Описание структуры запроса для метода создания задания.
    """
    model_config = ConfigDict(populate_by_name=True)

    title: str
    course_id: str = Field(alias="courseId")
    max_score: int = Field(alias="maxScore")
    min_score: int = Field(alias="minScore")
    order_index: int = Field(alias="orderIndex")
    description: str
    estimated_time: str = Field(alias="estimatedTime")

class UpdateExerciseRequestSchema(BaseModel):
    """
    Описание структуры запроса для метода обновления задания.
    """
    model_config = ConfigDict(populate_by_name=True)

    title: str | None
    max_score: int | None = Field(alias="maxScore")
    min_score: int | None = Field(alias="minScore")
    order_index: int | None = Field(alias="orderIndex")
    description: str | None
    estimated_time: str | None = Field(alias="estimatedTime")

class ExerciseSchema(BaseModel):
    """
    Описание структуры задания.
    """
    model_config = ConfigDict(populate_by_name=True)

    id: str
    title: str
    course_id: str = Field(alias="courseId")
    max_score: int = Field(alias="maxScore")
    min_score: int = Field(alias="minScore")
    order_index: int = Field(alias="orderIndex")
    description: str
    estimated_time: str = Field(alias="estimatedTime")

class GetExerciseResponseSchema(BaseModel):
    """
    Описание структуры ответа создание | получение | обновление задания.
    """
    exercise: ExerciseSchema

class GetExercisesResponseSchema(BaseModel):
    """
    Описание структуры запроса на получение списка заданий.
    """
    exercises: list[ExerciseSchema]

class CreateExerciseResponseSchema(BaseModel):
    """
    Описание структуры ответа создание | получение | обновление задания.
    """
    exercise: ExerciseSchema

class UpdateExerciseResponseSchema(BaseModel):
    """
    Описание структуры ответа создание | получение | обновление задания.
    """
    exercise: ExerciseSchema