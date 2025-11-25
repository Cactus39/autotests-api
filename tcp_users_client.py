import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
url = ("localhost", 12345)
client.connect(url)

client.send('Привет, сервер!'.encode())
response = client.recv(1024).decode()
client.close()

print(response)