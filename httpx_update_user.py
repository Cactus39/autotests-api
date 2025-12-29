import httpx
from tools.fakers import fake 
url_base = f"http://localhost:8000/api/v1"
url_login = "authentication/login"
url_user = "users"

payload_user = {
  "email": fake.email(),
  "password": "password",
  "lastName": "string",
  "firstName": "string",
  "middleName": "string"
}
payload_patch_user = {
  "email": fake.email(),
  "lastName": "string",
  "firstName": "string",
  "middleName": "string"
}

# CREATE USER
response_create_user = httpx.post(f"{url_base}/{url_user}", json=payload_user)
print(response_create_user.status_code)
user_id = response_create_user.json()['user']['id']

# LOGIN
response_login = httpx.post(f"{url_base}/{url_login}", json={"email": payload_user["email"],
                                                             "password": payload_user["password"]})
print(response_login.status_code)
access_token = response_login.json()['token']["accessToken"]
authorization_headers = {"Authorization": f"Bearer {access_token}"}

# PATCH
response_patch = httpx.patch(f"{url_base}/{url_user}/{user_id}", headers=authorization_headers, json=payload_patch_user)
print(response_patch.status_code)