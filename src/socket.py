#!/usr/bin/env python
from msg import InputMsg, OutputMsg
from gripper import Robotiq2F85 
# from pymodbus.client import ModbusSerialClient
import time
import threading

class SocketHandler:
    def __init__(self):
        # Gripper is a 2F with a TCP connection
        # TODO: add other types of gripper handling here
        self._gripper = Robotiq2F85()

    def getGripper(self):
        """Returns the configured gripper object
        """
        return self._gripper


print(f"TEST SOCKET HANDLER")
test = SocketHandler()
print(f"TEST SOCKET GRIPPER INTERPRETER: {test.getGripper().getInterpreter()}")
print(f"TEST SOCKET GRIPPER CLIENT: {test.getGripper().getClient()}")


