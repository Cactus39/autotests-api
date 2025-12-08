from clients.users.public_users_client import get_public_users_client, CreateUserRequestDict
from tools.fake_email import get_random_email
from clients.private_http_builder import AuthenticationUserDict
from clients.files.files_client import get_files_client, CreateFileRequestDict
from clients.courses.courses_client import get_courses_client, CreateCourseRequestDict
from clients.exercises.exercises_client import get_exercises_client, CreateExerciseRequestDict

public_users_client = get_public_users_client()


### Creating user
create_user_request = CreateUserRequestDict(lastName="str",
                                          middleName="str",
                                          firstName="str",
                                          email=get_random_email(),
                                          password="string"
                                          )

create_user_response = public_users_client.create_user(create_user_request)
print("Create user data:", create_user_response)

authenticate_user = AuthenticationUserDict(email=create_user_request["email"],
                                        password=create_user_request["password"])


### Creating file
create_file_request = CreateFileRequestDict(filename="test_file",
                                            directory="test_dir",
                                            upload_file="./testdata/test_file.png"
                                            )

create_file_response = get_files_client(authenticate_user).create_file(create_file_request)
print("Create file data:", create_file_response)


### Creating course
create_course_request = CreateCourseRequestDict(title="test_course",
                                                maxScore= 100,
                                                minScore= 0,
                                                description= "test_description",
                                                estimatedTime= "string",
                                                previewFileId= create_file_response["file"]["id"],
                                                createdByUserId= create_user_response["user"]["id"]
                                                )

create_course_response = get_courses_client(authenticate_user).create_course(create_course_request)
print("Create course data:", create_course_response)


### Creating exercise
create_exercise_request = CreateExerciseRequestDict(title= "test_exercise",
                                                    courseId= create_course_response["course"]["id"],
                                                    maxScore= 100,
                                                    minScore= 0,
                                                    orderIndex=1,
                                                    description= "test_description",
                                                    estimatedTime= "string"
                                                    )

create_exercise_response = get_exercises_client(authenticate_user).create_exercise(create_exercise_request)
print("Create exercise data:", create_exercise_response)



















