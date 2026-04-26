from functools import partial
from typing import Callable
import asyncio, websockets
import json
import log

SERVER_VERSION = "0.0.1"
SERVER_CAPABILITIES = []


async def main_loop(websocket: websockets.ServerConnection, session: dict):
    async for message in websocket:
        msg = json.loads(message)
        msg_type = msg.get("type")

        if msg_type == "state":
            pass

        else:
            log.info(f"Unknown message type: {msg_type}")


async def init_handler(on_request, websocket: websockets.ServerConnection):
    log.info("Request handshake")
    
    # Handle input
    msg = await websocket.recv()
    client_hello = json.loads(msg)

    if client_hello.get("type") != "hello":
        log.info("Client didnt send hello, disconnecting")
        return
    
    client_capabilities = client_hello.get("capabilities", [])
    log.info("Turtle connected: {capabilities: "+str(client_capabilities)+"}")

    # Give output

    await websocket.send(json.dumps({
        "type": "hello",
        "version": SERVER_VERSION,
        "capabilities": SERVER_CAPABILITIES
    }))

    session = {
        "capabilities": client_capabilities
    }

    # Start connection

    async for message in websocket:
        msg = json.loads(message)

        if msg.get("type") == "ping":
            await websocket.send(json.dumps({"type": "pong"}))
        
        elif msg.get("type") == "tick":
            await websocket.send(str(on_request(msg, session, message)))
        
        else:
            log.info(f"Unknown message type: {msg.get("type")}")
            await websocket.send(f"Unknown message type: {msg.get("type")}")


async def start(on_request:Callable[dict, dict], host:str = "0.0.0.0", port: int=8765):
    handler = partial(init_handler, on_request)

    async with websockets.serve(handler, host, port) as serv:
        log.info(f"Server running on {host}:{port}")
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(start(main_loop))