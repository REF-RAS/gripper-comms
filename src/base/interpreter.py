#!/usr/bin/env python
from abc import ABC, abstractmethod
from typing import TypeVar, Generic

T = TypeVar("T")
class Interpreter(ABC, Generic[T]):
    def __init__(self):
        pass

    @abstractmethod
    def verify(self, command: T):
        """Verifies a given command based on a known interpreter
        """
        pass

    @abstractmethod
    def refresh(self, command: T):
        """Refreshes command to be sent 
        """
        pass



