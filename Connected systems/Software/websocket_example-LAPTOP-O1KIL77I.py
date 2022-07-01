import asyncio
import websockets

async def handle_WS(websocket, uri):
    print(f"Connection accepted from {uri}")
    while True:
        try:
            data = await websocket.recv()
        except:
            print(f"Connection lost to {uri}")
            return
        print(f"Received {data} from {uri}")

server = websockets.serve(handle_WS, "", 8000)
asyncio.get_event_loop().run_until_complete(server)
asyncio.get_event_loop().run_forever()

"""
JavaScript:

let ws = new WebSocket("ws://localhost:8000");
ws.send("hallo");
ws.close();
"""