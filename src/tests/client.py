import asyncio
import websockets


async def send():
    uri = "ws://172.27.97.46:8766"
    async with websockets.connect(uri) as websocket:
        print("abc")
        await websocket.send("Hello world!")
        await websocket.recv()


asyncio.get_event_loop().run_until_complete(send())
