from tools.assertions.schema import validate_json_schema
from clients.users.public_users_client import get_public_users_client
from clients.users.private_users_client import get_private_users_client
from clients.private_http_builder import AuthenticationUserSchema
from clients.users.user_schema import GetUserResponseSchema, CreateUserRequestSchema
from tools.fake_email import get_random_email

create_user_request = CreateUserRequestSchema(firstName='str',
                                              lastName='str',
                                              middleName='str',
                                              password='str',
                                              email=get_random_email(),
                                              )
login_user = AuthenticationUserSchema(email=create_user_request.email,
                                    password=create_user_request.password)

public_client = get_public_users_client()

# Создаст пользователя с помощью метода API клиента PublicUsersClient.create_user.
user_id = public_client.create_user(create_user_request).user.id
private_client = get_private_users_client(user=login_user)

#Выполнит запрос на получение данных о созданном пользователе с использованием метода API клиента PrivateUsersClient.get_user_api
response = private_client.get_user_api(user_id)

#Провалидирует JSON schema ответа эндпоинта GET /api/v1/users/{user_id} (метод PrivateUsersClient.get_user_api).
validate_json_schema(instance=response.json(), schema=GetUserResponseSchema.model_json_schema(by_alias=True))
