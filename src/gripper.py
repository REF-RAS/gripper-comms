#!/usr/bin/env python
from robotiq.msg import InputMsg, OutputMsg
from robotiq.interpreter import RobotiqInterpreter
from robotiq.client import RobotiqClient
from base.interpreter import Interpreter
from base.client import Client 
import time
import threading

# NOTE: this should be a generic class that is configured for a particular interpreter and client from config
class GripperHandler:
    def __init__(self):
        # Gripper is a 2F with a TCP connection
        # TODO: add other types of gripper handling here
        self._interpreter: Interpreter = RobotiqInterpreter()
        self._client: Client = RobotiqClient()

    def getInterpreter(self):
        return self._interpreter

    def getClient(self):
        return self._client

print(f"TEST GRIPPER HANDLER") 
gripper = GripperHandler()
client = gripper.getClient()
client.connect()
print(f"TEST GRIPPER INTERPRETER: {gripper.getInterpreter()}")
print(f"TEST GRIPPER CLIENT: {client.status(9)}")


