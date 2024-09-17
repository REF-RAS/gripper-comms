#!/usr/bin/env python
# -- Robotiq specific
from robotiq.interpreter import RobotiqInterpreter
from robotiq.client import RobotiqClient
from robotiq.interface import GrasshopperInterface
# -- Base
from base.interface import Interface 
from base.interpreter import Interpreter
from base.client import Client 
import time
from threading import Thread, Lock
from queue import Queue

# NOTE: this should be a generic class that is configured for a particular interpreter and client from config
class GripperHandler:
    def __init__(self):
        # -- Prepare main object varibales for use
        # These are parsed in object types for instantiation
        self._interpreter: Interpreter = None
        self._client: Client = None
        self._interface: Interface = None
        # These are the instantiated object handlers
        self._client_handler = None
        self._interpreter_handler = None
        # Prepare comms between threads
        self._input_q: Queue = Queue()
        self._output_q: Queue = Queue()
        self._lock: Lock = Lock()
        # This will be updated to control thread for websocket
        self._interface_run: bool = True 
        self._interface_connection: bool = False
        self._interface_thread = None

    def __del__(self):
        self._stop_threads()

    # -- Private Methods (or abstraction methods)
    def _run_check_method(self):
        """Thread method for getting class web socket run boolean
        """
        with self._lock:
            return self._interface_run

    def _connection_check_method(self, value: bool):
        """Thread method for updating class web socket connection boolean
        """
        with self._lock:
            self._interface_connection = value

    def _stop_threads(self):
        print(f"[GRIPPER] Stopping Threads")
        self._web_socket_run = False
        if self._interface_thread is not None and self._interface_thread.is_alive():
            print(f"[GRIPPER] Stopping {self._interface_thread.name}")
            self._interface_thread.join(1)

    # -- Public Methods
    def run(self):
        # Main thread operation
        # - Get messages from the interface thread 
        #   this may be commands from the interface (for action)
        #   or it could be state changing information (i.e. close of socket)
        while True:
            try:
                # Blocking wait for interface data
                print(f"[GRIPPER] Waiting for Interface Data")
                interface_data = self._input_q.get(block=True)
                print(f"[GRIPPER] Interface Data is {interface_data}")
                # The interface data can be of any length as a dict 
                for key in interface_data.keys():
                    if key == 'termination':
                        # Handle interface temination (i.e., resetup for next connection)
                        print(f"[GRIPPER] Interface has Terminated. Handling Initialisation for new Connections")
                        self._interface_init()
                    elif key == 'command':
                        # A command was received from interface, parse and send to gripper
                        # Get the gripper status here, we can send this back to the main thread for parsing
                        # Generate the command to send to the gripper and send said command (now in main thread)
                        gripper_command = self._interpreter_handler.generate(interface_data[key])
                        prepared_gripper_command = self._interpreter_handler.refresh(gripper_command)
                        self._client_handler.send(prepared_gripper_command)
                    else:
                        print(f"[GRIPPER ERROR] Unknown Interface State {key}")

                time.sleep(1)
            except KeyboardInterrupt:
                break

        self._stop_threads()

    def setup(self):
        if self._interface is None:
            print(f"[GRIPPER ERROR] Interface not defined {self._interface}")
            return

        if self._interpreter is None:
            print(f"[GRIPPER ERROR] Interpreter not defined")
            return

        if self._client is None:
            print(f"[GRIPPER ERROR] Client not defined")
            return

        # Create the control interface and start its thread
        self._interface_thread = Thread(
            target=self._interface, 
            args=(
                self._input_q,
                self._output_q,
                self._run_check_method,
                self._connection_check_method,
                ),
            daemon=True
        )
        self._interface_thread.start()
        self._interface_thread.name = "Thread-Control-Interface"

        # Create the interpreter for the gripper client comms
        self._interpreter_handler = self._interpreter()

        # Create the client for the gripper (comms to gripper)
        self._client_handler = self._client()
        # TODO: test connection
        self._client_handler.connect()

        # Setup any initialisation in the interface
        self._interface_init()

    def _interface_init(self):
        # NOTE: This may be custom based on type of gripper
        # -- Send the status of the gripper
        # Get the gripper's status via the gripper client
        gripper_status = self._client_handler.status()
        # Interpret message into required format for usage in interface
        interpreted_gripper_status = self._interpreter_handler.interpret(gripper_status)
        # Put the interpreted_gripper_status into the interface thread for usage
        self._output_q.put(interpreted_gripper_status)


    @property
    def interface(self):
        """The interface property."""
        return self._interface

    @interface.setter
    def interface(self, value: Interface):
        self._interface = value

    @property
    def interpreter(self):
        """The interpreter property.
        """
        return self._interpreter

    @interpreter.setter
    def interpreter(self, value: Interpreter):
        self._interpreter = value

    @property
    def client(self):
        """The _client property.
        """
        return self._client

    @client.setter
    def client(self, value: Client):
        self._client = value

if __name__ == "__main__":
    # EXPECTED FUNCTIONALITY
    # On run, should instantiate gripper type based on config read
    # Run a thread to handle connection to the gripper
    # Run a thread to handle socket connection to Grasshopper
    # If either thread has a connection issue, the other should run independently
    # TODO: add any argument parsing if needed
    # Setup the gripper and Object types 
    gripper = GripperHandler()
    # TODO: implement configuration read here for these types
    gripper.interpreter = RobotiqInterpreter
    gripper.client = RobotiqClient
    gripper.interface = GrasshopperInterface
    
    # Setup the Gripper
    gripper.setup()

    # Run the Gripper
    gripper.run()








