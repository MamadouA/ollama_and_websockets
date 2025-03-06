import asyncio
import ssl
from websockets.asyncio.server import serve
from websockets.exceptions import ConnectionClosed
import ollama

# Le nom du model d'IA utilisée
model_name = "llama3.2"

context = [
        {
            "role": "assistant", 
            "content":  
                """
                    Vous êtes un assistant IA qui ne répond que de manière très concise.
                    Répondez toujours en une ou deux phrases maximum.
                    Si une question n'est pas liée à l'informatique, répondez par 
                    'Je suis désolé, mais je ne peux répondre qu'aux questions en 
                    en rapport avec l'informatique'.
                """
        }
    ]

async def handler(websocket):
    while True:
        try:
            # Reception d'un message
            message = await websocket.recv()

            # Ajout du message dans l'historique de la conversation
            context.append({"role": "user", "content": message})

            # Envoie du context au model 
            response = ollama.chat(model=model_name, messages=context)
            
            # Ajout de la réponse du model dans l'historique de la conversation
            context.append({"role": "assistant", "content": response["message"]["content"]})

            # Envoie de la réponse du model au client
            await websocket.send(response["message"]["content"])

        except ConnectionClosed:
            print("...Un client s'est déconnecté")
            break


# Charger le certificat SSL et la clé privée
ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
ssl_context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")

async def main():
    async with serve(handler, "localhost", 8000, ping_timeout=120, ssl=ssl_context) as server:
        print("Serveur en cours sur wss://localhost:8000")
        await server.serve_forever()


asyncio.run(main())