#!/usr/bin/env python
import asyncio
import websockets
import os
from threading import Thread
from queue import Queue, Empty
from base.interface import Interface 
from grippers.robotiq.msg import InputMsg

class GrasshopperInterface(Interface):
    def __init__(self, input_q: Queue, output_q: Queue, run_control_method, connection_check_method, port: int = 8001):
        super().__init__()
        self._input_q: Queue = input_q 
        self._output_q: Queue = output_q 
        self._run_control_method = run_control_method
        self._connection_check_method = connection_check_method
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
        print(f"[INTERFACE] WebSocket Interface Initialising")
        # Initialising requires getting the grippers status
        gripper_status = self._output_q.get()
        if isinstance(gripper_status, InputMsg):
            prev_msg = int(gripper_status.gPO)
        else:
            prev_msg = 0

        print(f"[INTERFACE] Gripper status is: {gripper_status} | prev_msg is {prev_msg}")
        self_termination: bool = False
        # Loop functionality under main thread control
        print(f"[INTERFACE] Run control method: {self._run_control_method()}")
        while self._run_control_method():
            # Wait for a command from the Grasshopper interface
            try:
                message = await websocket.recv()
                print(f"[INTERFACE] Received: {message}")
                # TODO: Verify this from the current functionality
                # if len(message) > 0 and abs(int(message) - prev_msg) > 5:
                # Send message in a dict for easy interpretation
                self._input_q.put({'command': message})
                # TODO: Verify this from the current functionality
                # prev_msg = int(message)
            except websockets.ConnectionClosedOK:
                self_termination = True
                break

        print(f"[INTERFACE] WebSocket Reached End...Self Termination Status: {self_termination}")
        self._input_q.put({'termination': self_termination})
        return
