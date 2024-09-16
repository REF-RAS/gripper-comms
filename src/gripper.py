#!/usr/bin/env python
# -- Robotiq specific
from robotiq.interpreter import RobotiqInterpreter
from robotiq.client import RobotiqClient
from robotiq.controller import GrasshopperController 
# -- Base
from base.controller import Controller
from base.interpreter import Interpreter
from base.client import Client 
import time
from threading import Thread, Lock
from queue import Queue

# NOTE: this should be a generic class that is configured for a particular interpreter and client from config
class GripperHandler:
    def __init__(self):
        # Gripper is a 2F with a TCP connection
        # TODO: add other types of gripper handling here
        self._interpreter: Interpreter = None
        self._client: Client = None
        self._controller: Controller = None
        self._input_q: Queue = Queue()
        self._output_q: Queue = Queue()
        self._lock: Lock = Lock()
        # This will be updated to control thread for websocket
        self._web_socket_run: bool = True 
        self._web_socket_connection: bool = False
        self._controller_thread = None

    # -- Private Methods (or abstraction methods)
    def _run(self):
        """Thread method for getting class web socket run boolean
        """
        with self._lock:
            return self._web_socket_run

    def _connected(self, value: bool):
        """Thread method for updating class web socket connection boolean
        """
        with self._lock:
            self._web_socket_connection = value

    async def _controller_handler(self):
        print(f"Socket Handler Initialising")
        # while True:
        recieved = await websocket.recv()

        print(f"Socket Terminating...")
        return

    def _stop_threads(self):
        print(f"[GRIPPER] Stopping Threads")
        self._web_socket_run = False
        if self._controller_thread is not None and self._controller_thread.is_alive():
            print(f"[GRIPPER] Stopping {self._controller_thread.name}")
            self._controller_thread.join(1)

    # -- Public Methods
    def run(self):
        while True:
            time.sleep(1)

    def controller_setup(self, controller):
        self._controller_thread = Thread(
            target=controller, 
            args=(
                self._input_q,
                self._output_q,
                self._run,
                self._connected,
                8001
                ),
            daemon=True
        )
        self._controller_thread.start()
        self._controller_thread.name = "Thread-Grasshopper-Websocket"

    @property
    def interpreter(self):
        """The interpreter property.
        """
        return self._interpreter

    @interpreter.setter
    def interpreter(self, value: Interpreter):
        if not isinstance(value, Interpreter):
            return
        self._interpreter = value

    @property
    def client(self):
        """The _client property.
        """
        return self._client

    @client.setter
    def client(self, value: Client):
        if not isinstance(value, Client):
            return
        self._client = value

if __name__ == "__main__":
    # TODO: add any argument parsing if needed
    # TODO: implement configuration read here

    # Setup the gripper and connections
    gripper = GripperHandler()
    gripper.interpreter = RobotiqInterpreter()
    gripper.client = RobotiqClient()
    gripper.controller_setup(controller=GrasshopperController)

    print(f"GRIPPER INTERPRETER: {gripper.interpreter}")
    print(f"GRIPPER CLIENT: {gripper.client}")

    gripper._stop_threads()

    # EXPECTED FUNCTIONALITY
    # On run, should instantiate gripper type based on config read
    # Run a thread to handle connection to the gripper
    # Run a thread to handle socket connection to Grasshopper
    # If either thread has a connection issue, the other should run independently







