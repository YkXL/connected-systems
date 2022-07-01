import asyncio
import websockets

async def handle_WS(websocket, uri):
    print(f"Connection accepted from {uri}")
    i = 1
    while True:
        try:
            data = await websocket.recv()
        except:
            print(f"Connection lost to {uri}")
            return
        if data == "request_messages":
            await websocket.send(f"Here is message number {i}")
            i += 1


server = websockets.serve(handle_WS, "", 8000)
asyncio.get_event_loop().run_until_complete(server)
asyncio.get_event_loop().run_forever()
