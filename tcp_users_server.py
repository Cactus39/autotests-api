import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
url = ("localhost", 12345)
server.bind(url)

server.listen(10)
message_list = []

while 1:
    try:
        client, addr = server.accept()
        print(f"Пользователь с адресом: {addr} подключился к серверу")
        message = client.recv(1024)
        message = message.decode()
        message_list.append(message)
        print(f"Пользователь с адресом: {addr} отправил сообщение: {message}")
        client.send('\n'.join(message_list).encode())
    except KeyboardInterrupt:
        break
server.close()