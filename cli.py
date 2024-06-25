import asyncio
import websockets
import ssl
import json

WS_URL = 'wss://127.0.0.1/ws/test/'

async def send_message(websocket, event, state):
    await websocket.send(json.dumps({'event': event, 'state': state}))

async def cli():
    ssl_context = ssl._create_unverified_context()  # Create an unverified SSL context
    async with websockets.connect(WS_URL, timeout=60, ssl=ssl_context) as websocket:
        print("Connected to", WS_URL)
        while True:
            command = input("Enter command: (pause/resume/exit)")
            if command == "pause":
                await send_message(websocket, "isPaused", True)
            elif command == "resume":
                await send_message(websocket, "isPaused", False)
            elif command == "exit":
                break
            else:
                print("Invalid command")

if __name__ == "__main__":
    asyncio.run(cli())
