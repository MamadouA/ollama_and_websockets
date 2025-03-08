import asyncio
from websockets.asyncio.client import connect

# Réception et envoie des messages
async def handle_message():
    async with connect("ws://localhost:8000", ping_timeout=120) as websocket:

        while True:
            print()
            message = input("Entrez votre message: ")
      
            await websocket.send(message)

            message = await websocket.recv()
            print(message, end="\n")

# Run the client
asyncio.run(handle_message())
