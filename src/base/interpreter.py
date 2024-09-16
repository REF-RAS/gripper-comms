#!/usr/bin/env python
from abc import ABC, abstractmethod

class Interpreter(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def _verify(self, command):
        """Verifies a given command based on a known interpreter
        """
        pass

    @abstractmethod
    def _refresh(self, command):
        """Refreshes command to be sent 
        """
        pass



