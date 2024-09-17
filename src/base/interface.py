#!/usr/bin/env python
from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Callable
from queue import Queue

T = TypeVar("T")
Func = Callable[[T], bool]
class Interface(ABC, Generic[T]):
    def __init__(
            self, 
            input_q: Queue, 
            output_q: Queue, 
            run_control_method: Func[T], 
            connection_check_method: Func[T]
        ):
        # This is a method/object that controls if the interface runs or not
        self._run_control_method: Func[T] = run_control_method
        # This is a method/object that checks if the interface is connected or not
        self._connection_check_method: Func[T] = connection_check_method
        # Expected Queue variables for interface thread communication
        self._input_q: Queue = input_q
        self._output_q: Queue = output_q

    @abstractmethod
    def _setup(self):
        """A required setup method for the interface 
        """
        pass

    @abstractmethod
    def _interface_handler(self):
        """This is the main interface handler 
        """
        pass

