#!/usr/bin/env python
from abc import ABC, abstractmethod
from typing import TypeVar, Generic

T = TypeVar("T")
class Client(ABC, Generic[T]):
    def __init__(self):
        self._connection_status: bool = False

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
    def status(self) -> T:
        """Return the status from client
        """
        pass
