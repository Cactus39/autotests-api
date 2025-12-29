from clients.users.public_users_client import get_public_users_client
from clients.users.user_schema import CreateUserRequestSchema
from clients.private_http_builder import AuthenticationUserSchema
from clients.files.files_client import get_files_client
from clients.files.files_schema import CreateFileRequestSchema
from clients.courses.courses_client import get_courses_client
from clients.courses.courses_schema import CreateCourseRequestSchema
from clients.exercises.exercises_client import get_exercises_client
from clients.exercises.exercises_schema import CreateExerciseRequestSchema

public_users_client = get_public_users_client()

### Creating user
create_user_request = CreateUserRequestSchema()

create_user_response = public_users_client.create_user(create_user_request)
print("Create user data:", create_user_response)

authentication_user = AuthenticationUserSchema(email=create_user_request.email,
                                        password=create_user_request.password)

### Creating file
create_file_request = CreateFileRequestSchema(upload_file="./testdata/test_file.png")
files_client = get_files_client(authentication_user)
create_file_response = files_client.create_file(create_file_request)
print("Create file data:", create_file_response)


### Creating course
create_course_request = CreateCourseRequestSchema(preview_file_id= create_file_response.file.id,
                                                created_by_user_id= create_user_response.user.id
                                                )

courses_client = get_courses_client(authentication_user)
create_course_response = courses_client.create_course(create_course_request)
print("Create course data:", create_course_response)


### Creating exercise
create_exercise_request = CreateExerciseRequestSchema(course_id= create_course_response.course.id)

exercises_client = get_exercises_client(authentication_user)
create_exercise_response = exercises_client.create_exercise(create_exercise_request)
print("Create exercise data:", create_exercise_response)



















