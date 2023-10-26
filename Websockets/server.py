import asyncio
import websockets

connected = set()

async def echo(websocket, path):
    connected.add(websocket)
    try:
        print("Connected to a new client.")
        async for message in websocket:
            print(f"Received: {message}")
            outbound_ws = [ws for ws in connected if ws != websocket]
            if outbound_ws:
                await asyncio.wait([ws.send(message) for ws in outbound_ws])
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        await websocket.close()

if __name__ == "__main__":
    print('websocket server initialized')
    loop = asyncio.get_event_loop()
    loop.run_until_complete(websockets.serve(echo, 'localhost', 8765))
    loop.run_forever()
