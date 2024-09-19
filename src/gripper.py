#!/usr/bin/env python
from base import *
from grippers import *
from threading import Thread, Lock
from queue import Queue
import time, yaml, os, importlib

# Set the path to be the root of this package
__path__ = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))

# NOTE: this should be a generic class that is configured for a particular interpreter and client from config
class GripperHandler:
    def __init__(self):
        """Constructor
        """
        # -- Prepare main object varibales for use
        # These are parsed in object types for instantiation
        self._interpreter: Interpreter = None
        self._client: Client = None
        # Prepare comms between threads
        self._input_q: Queue = Queue()
        self._output_q: Queue = Queue()
        self._lock: Lock = Lock()
        # This will be updated to control thread for websocket
        self._interface_run: bool = True 
        self._interface_connection: bool = False
        self._interface_thread: Thread = None

    def __del__(self):
        """Destructor
        """
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

    def _client_connection_check(self): 
        # attempt to connect to client
        # If client is connected, update main thread
        # If the client is disconnected, update main thread 
        # Handle loop of 1 second (on checks)
        pass

    def _stop_threads(self):
        """Stops any running threads
        """
        print(f"[GRIPPER] Stopping Threads")
        if self._interface_thread is not None and self._interface_thread.is_alive():
            print(f"[GRIPPER] Stopping {self._interface_thread.name}")
            self._interface_thread.join(1)

    # -- Public Methods
    def run(self):
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
                        # check if the gripper is connected or not prior to proceeding
                        if not self._client._connected:
                            # Reset Procedure
                            self.setup()
                        
                        # A command was received from interface, parse and send to gripper
                        # Generate the command to send to the gripper and send said command (now in main thread)
                        gripper_command = self._interpreter.generate_output(interface_data[key])
                        self._client.send(gripper_command)
                    else:
                        print(f"[GRIPPER ERROR] Unknown Interface State {key}")

                time.sleep(1)
            except KeyboardInterrupt:
                break

        self._stop_threads()

    def create(self):
        # Read config and extract names
        with open(__path__ + "/config/gripper.yaml", 'r') as f:
            config = yaml.safe_load(f)
        
        # The main module for all object creators
        module = importlib.import_module('grippers')

        # Create the interpreter for the gripper client comms
        self._interpreter = getattr(module, config['interpreter'])()
        # Create the client for the gripper (comms to gripper)
        self._client = getattr(module, config['client'])()

        # Create the control interface and start its thread
        self._interface_thread = Thread(
            target=getattr(module, config['interface']), 
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

    def setup(self):
        """Setup procedure for the gripper
        TODO: this is currently too custom to the type of gripper, so package into gripper type if possible
        """
        # TODO: test connection
        self._client.connect()
        print(f"[GRIPPER] Initialising...")
        self._client.send(self._interpreter.generate_output('r'))
        time.sleep(1)
        self._client.send(self._interpreter.generate_output('a'))
        time.sleep(1)

        # Setup any initialisation in the interface
        self._interface_init()

    def _interface_init(self):
        # NOTE: This may be custom based on type of gripper
        # -- Send the status of the gripper
        # Get the gripper's status via the gripper client
        # gripper_status = self._client_handler.status()
        # Interpret message into required format for usage in interface
        # interpreted_gripper_status = self._interpreter_handler.interpret(gripper_status)
        # Put the interpreted_gripper_status into the interface thread for usage
        # self._output_q.put(interpreted_gripper_status)
        pass

if __name__ == "__main__":
    # EXPECTED FUNCTIONALITY
    # On run, should instantiate gripper type based on config read
    # Run a thread to handle connection to the gripper
    # Run a thread to handle socket connection to Grasshopper
    # If either thread has a connection issue, the other should run independently
    # TODO: add any argument parsing if needed
    # Setup the gripper and Object types 
    gripper = GripperHandler()
    gripper.create()
    # TODO: implement factory read here for these types
    # gripper.interpreter = RobotiqInterpreter
    # gripper.client = RobotiqClient
    # gripper.interface = GrasshopperInterface
    
    # Setup the Gripper
    gripper.setup()

    # Run the Gripper
    gripper.run()








