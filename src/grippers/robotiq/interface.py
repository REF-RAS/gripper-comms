#!/usr/bin/env python
import asyncio
import websockets
import os
from threading import Thread
from queue import Queue, Empty
from typing import Callable 
from base.interface import Interface 

class GrasshopperInterface(Interface):
    def __init__(
            self,  
            input_q: Queue, 
            output_q: Queue, 
            run_control_method: Callable, 
            connection_check_method: Callable, 
            port: int = 8001
        ):
        print(f"[INTERFACE] Grasshopper Type Instantiated")
        super().__init__(
            input_q=input_q,
            output_q=output_q,
            run_control_method=run_control_method, 
            connection_check_method=connection_check_method
        )
        self._port = port
        self._loop = None

        # Run the setup process
        self._setup()

    def _setup(self):
        # Setup asyncio event loop
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)

        # Attempt to start socket serve
        started = False
        while not started:
            try:
                print(f"[INTERFACE] Trying to Establish WebSocket Connection...")
                server = websockets.serve(self._interface_handler, "localhost", self._port)
                self._loop.run_until_complete(server)
                started = True
            except OSError as e:
                print(f"[INTERFACE] Cannot Connect to Port {port} ")
                break

        if not started:
            print(f"[INTERFACE] Failed to Setup")
        else:
            self._loop.run_forever()

        print(f"[INTERFACE] Reached end of Setup")

    async def _interface_handler(self, websocket):
        """This is the main interface input/output method
        Expected to be run in a Thread
        """
        print(f"[INTERFACE] WebSocket Interface Initialising")
        self_termination: bool = False
        # Loop functionality under main thread control
        print(f"[INTERFACE] Run control method: {self._run_control_method()}")
        while self._run_control_method():
            # Wait for a command from the Grasshopper interface
            try:
                message = await websocket.recv()
                print(f"[INTERFACE] Received: {message}")
                self._input_q.put({'command': message})
            except websockets.ConnectionClosedOK:
                self_termination = True
                break

        print(f"[INTERFACE] WebSocket Reached End...Self Termination Status: {self_termination}")
        self._input_q.put({'termination': self_termination})
        return
