#!/usr/bin/env python
from abc import ABC, abstractmethod
from typing import TypeVar, Generic

T = TypeVar("T")
class Controller(ABC, Generic[T]):
    def __init__(self):
        # This is a method that updates if the main program requests a termination or not
        self._run: T = None 
        # This is a method that is updated on the socket's connection status for reference
        # on the main thread
        self._connected: T = None 
        # Queue variables
        self._input_q: Queue = None 
        self._output_q: Queue = None 

    @abstractmethod
    def _controller_handler(self):
        pass

