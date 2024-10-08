#!/usr/bin/env python
# Copyright 2024 - Dasun Gunasinghe
# Research Engineering Facility, Queensland University of Technology (QUT)
__author__ = 'Dasun Gunasinghe'
__email__ = 'robotics.ref@qut.edu.au'

from abc import ABC, abstractmethod
from typing import TypeVar, Generic

T = TypeVar("T")
class Interpreter(ABC, Generic[T]):
    def __init__(self):
        pass

    @abstractmethod
    def verify_output(self, command: T) -> T:
        """Verifies a given output command based on a known interpreter
        """
        pass

    @abstractmethod
    def generate_output(self, command: T) -> T:
        """Generates an output command to be sent in known message format 
        """
        pass

    @abstractmethod
    def interpret_input(self, command: T) -> T:
        """Interprets an input and outputs in known message format 
        """
        pass

T = TypeVar("T")
class Client(ABC, Generic[T]):
    def __init__(self, interpreter: Interpreter):
        self._connection_status: bool = False
        self._interpreter: Interpreter = interpreter

    # -- Standard Methods
    def get_interpreter(self) -> Interpreter:
        return self._interpreter

    # -- Properties
    @property
    def _connected(self):
        """The _connection_status property.
        """
        return self._connection_status

    @_connected.setter
    def _connected(self, value: bool = False):
        """Setting the _connection_status property
        """
        self._connection_status = value

    # -- Abstract Methods
    @abstractmethod
    def setup(self) -> T:
        """Conducts required setup for the client
        """
        pass

    @abstractmethod
    def send(self, command: T) -> bool:
        """Sends the command to a client
        """
        pass

    @abstractmethod
    def connect(self) -> bool:
        """Connects to a client device
        """
        pass

    @abstractmethod
    def disconnect(self) -> T:
        """Disconnects from a client device 
        """
        pass

    @abstractmethod
    def get_status(self) -> T:
        """Return the status from client
        """
        pass

