import asyncio
import websockets

async def send_msg(websocket):
    while True:
        message = input("Type a message: ")
        if not message:
            break
        await websocket.send(message)

async def recv_msg(websocket):
    while True:
        response = await websocket.recv()
        print(f"Received: {response}")

async def main():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        await asyncio.gather(await send_msg(websocket), await recv_msg(websocket))

if __name__ == "__main__":
    print("websocket client initialized")
    asyncio.run(main())
