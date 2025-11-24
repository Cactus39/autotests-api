import asyncio
import websockets



async def client():
    url = "ws://localhost:8765"
    async with websockets.connect(url) as client_connection:
        message = "Привет, сервер!"

        await client_connection.send(message)


        for _ in range(5):

            response = await client_connection.recv()
            print(response)

asyncio.run(client())
