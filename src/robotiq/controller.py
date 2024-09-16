#!/usr/bin/env python
import asyncio
import websockets
import os
from threading import Thread
from queue import Queue, Empty
from base.controller import Controller

class GrasshopperController(Controller):
    def __init__(self, input_q, output_q, run, connected, port):
        super().__init__()
        self._input_q = input_q
        self._output_q = output_q
        self._run = run
        self._connected = connected
        self._port = port

        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)

        # Attempt to start socket serve
        started = False
        while not started:
            try:
                print(f"[WEBSOCKET] Trying to Establish Connection...")
                server = websockets.serve(self._controller_handler, "localhost", self._port)
                self._loop.run_until_complete(server)
                started = True
            except OSError as e:
                print(f"[WEBSOCKET] Cannot Connect to Port {port} ")
                break

        if not started:
            print(f"[WEBSOCKET] Failed to Setup")
        else:
            self._loop.run_forever()

        print(f"[WEBSOCKET] Reached end of Setup")

    def _additional_setup(self):
        pass

    async def _controller_handler(self, websocket):
        print(f"Socket Handler Initialising")
        # while True:
        recieved = await websocket.recv()

        print(f"Socket Terminating...")
        return


