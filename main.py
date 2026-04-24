import asyncio
import server

def on_request(data, session):
    print(f"data: {data}\nsession: {session}")
    return "";

asyncio.run(server.start(on_request))