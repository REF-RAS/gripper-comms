#!/usr/bin/env python
from abc import ABC, abstractmethod
from typing import TypeVar, Generic

T = TypeVar("T")
class Interface(ABC, Generic[T]):
    def __init__(self):
        # This is a method/object that controls if the interface runs or not
        self._run_control_method: T = None 
        # This is a method/object that checks if the interface is connected or not
        self._connection_check_method: T = None 
        # Expected Queue variables
        self._input_q: Queue = None 
        self._output_q: Queue = None 

    @abstractmethod
    def _interface_handler(self):
        """This is the main interface handler 
        """
        pass

