import ollama
import asyncio
from websockets.asyncio.server import serve
from websockets.exceptions import ConnectionClosed

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

async def main():
    print_chatbot_banner()

    async with serve(handler, "localhost", 8000, ping_timeout=120) as server:
        await server.serve_forever()

def print_chatbot_banner():
    banner = r'''
  ____ _           _     ____        _   
 / ___| |__   __ _| |_  | __ )  ___ | |_ 
| |   | '_ \ / _` | __| |  _ \ /   \| __|
| |___| | | | (_| | |_  | |_) | /-\ | |_| 
 \____|_| |_|\__,_|\__| |____/ \___/\__|
    
Serveur en écoute sur wss://localhost:8000
    '''
    print(banner)

asyncio.run(main())