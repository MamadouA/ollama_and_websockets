import asyncio
import ssl
from websockets.asyncio.client import connect

# Création d'un contexte SSL 
ssl_context = ssl.create_default_context()

# Désactivation de la vérification du certificat
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# Réception et envoie des messages
async def handle_message():
    async with connect("wss://localhost:8000", ping_timeout=120, ssl=ssl_context) as websocket:

        while True:
            message = input("Entrez votre message: ")
      
            await websocket.send(message)

            message = await websocket.recv()
            print(message, end="\n")

# Run the client
asyncio.run(handle_message())
