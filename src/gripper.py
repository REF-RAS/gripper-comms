#!/usr/bin/env python
# Copyright 2024 - Dasun Gunasinghe
# Research Engineering Facility, Queensland University of Technology (QUT)
__author__ = 'Dasun Gunasinghe'
__email__ = 'robotics.ref@qut.edu.au'

# -- Imports from Base Definition and Custom Extensions
from base import *
from grippers import *
# -- General imports
from threading import Thread, Lock
from queue import Queue
import time, yaml, os, importlib, signal, sys

# Set the path to be the root of this package
__path__ = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))

# NOTE: this should be a generic class that is configured for a particular interpreter and client from config
class GripperHandler:
    def __init__(self):
        """Constructor
        """
        # -- Prepare Signals
        signal.signal(signal.SIGINT, self._exit_gracefully)
        signal.signal(signal.SIGTERM, self._exit_gracefully)
        # -- Prepare main object varibales for use
        # The main client (gripper) object
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
        print(f"[GRIPPER] Destructor Terminating Gracefully")
        self._stop_threads()

    def _exit_gracefully(self, signum, frame):
        """Signal exit handling
        """
        print(f"[GRIPPER] Terminating Gracefully")
        self._stop_threads()
        sys.exit(0)

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

    # TODO: If desired
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
                # Blocking wait for interface data from interface thread implementation
                print(f"[GRIPPER] Waiting for Interface Data")
                interface_data = self._input_q.get(block=True)
                print(f"[GRIPPER] Interface Data is {interface_data}")
                # The interface data can be of any length as a dict 
                for key in interface_data.keys():
                    if key == 'termination':
                        # Handle interface temination (i.e., resetup for next connection)
                        print(f"[GRIPPER] Interface has Terminated. Handling Initialisation for new Connections")
                        # NOTE: placeholder for any additional functionaliy as desired
                    elif key == 'command':
                        # check if the gripper is connected or not prior to proceeding
                        if not self._client._connected:
                            # Reset Procedure Actioned by Gripper
                            self.setup()
                        
                        # Generate the command to send to the gripper and send said command (now in main thread)
                        gripper_command = self._client.get_interpreter().generate_output(interface_data[key])
                        self._client.send(gripper_command)
                    else:
                        print(f"[GRIPPER ERROR] Unknown Interface State {key}")

                time.sleep(1)
            except KeyboardInterrupt:
                break

        # If here, exit
        self._exit_gracefully()

    def create(self):
        # Read config and extract names
        with open(__path__ + "/config/gripper.yaml", 'r') as f:
            config = yaml.safe_load(f)
        
        # The main module for all object creators
        module = importlib.import_module('grippers')

        # Create the client for the gripper (comms to gripper)
        # Create the interpreter for the gripper client comms
        self._client = getattr(module, config['client'])(
            interpreter=getattr(module, config['interpreter'])()
        )

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
        """
        print(f"[GRIPPER] Initialising...")
        self._client.connect()
        self._client.setup()

if __name__ == "__main__":
    # EXPECTED FUNCTIONALITY
    # On run, should instantiate gripper type based on config read
    # [MAIN THREAD] Run a thread to handle connection to the gripper (client)
    # [NEW THREAD] Run a thread to handle connection to Interface (interface) 
    # If either thread has a connection issue, the other should run independently
    # Setup the gripper and Object types 
    gripper = GripperHandler()
    # Initialise gripper through factory method
    gripper.create()
    # Setup the Gripper
    gripper.setup()
    # Run the Gripper
    gripper.run()
