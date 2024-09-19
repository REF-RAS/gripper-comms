#!/usr/bin/env python
import websockets
import asyncio
import time

async def test_client():
    print(f"WebSocket Client Test")
    url = "ws://localhost:8001"
    async with websockets.connect(url) as ws:
        msg = 0
        await ws.send(f"{msg}")
        time.sleep(2)
        msg = 255
        await ws.send(f"{msg}")

        # Stay alive until self termination
        while True:
            msg = await ws.recv()
            print(msg)


# Start the client
asyncio.run(test_client())


