import httpx

url_post = "http://localhost:8000/api/v1/authentication/login"
url_get = "http://localhost:8000/api/v1/users/me"
payload_post = {
  "email": "user@example.com",
  "password": "password"
}


response = httpx.post(url_post, json=payload_post)
print(response.status_code)
access_token = response.json()['token']["accessToken"]
headers = {"Authorization": f"Bearer {access_token}"}
response = httpx.get(url_get, headers=headers)
print(response.status_code)

print(response.json())
