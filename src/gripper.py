#!/usr/bin/env python
import logging
from abc import ABC, abstractmethod


class Gripper(ABC):
    # -- Internal Methods
    def __init__(self, name):
        self._name = name
        self._message: list = []
        self._interpreter = None 
        self._client = None  
        self._logger = logging.getLogger(self._name)
        print(f"GRIPPER NAME: {self._name}")

    def _verify(self, command):
        """Verifies a given command based on a known
        interpreter
        """
        # Handle any error on interpreter not being defined
        if self._interpreter is None:
            print(f"")
            return

        # TODO: add functionality to verify given command against interpreter

    def _refresh(self, command):
        """Refreshes command to be sent 
        """
        pass

    def _send(self, command):
        """Sends the command to a client
        """
        pass

    def _status(self):
        """Return the status from client
        """
        pass

    # -- Public Facing Methods
    def setInterpreter(self, interpreter):
        """Sets the class interpreter for message sending and getting"""
        # TODO: add some check on type?
        self._interpreter = interpreter

    def getInterpreter(self):
        """Gets the configured interpreter object
        """
        return self._interpreter

    def setClient(self, client):
        """Sets the class client to send to
        """
        # TODO: add some check on type?
        self._client = client

    def getClient(self):
        """Gets the configured client object
        """
        return self._client

class Robotiq2F85(Gripper):
    def __init__(self):
        super().__init__(name='Robotiq2F85')
        # TODO: update placeholders with functionality
        self.setInterpreter(1)
        self.setClient(2)




