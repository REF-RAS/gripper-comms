#!/usr/bin/env python
from base.interpreter import Interpreter 

class RobotiqInterpreter(Interpreter):
    def __init__(self):
        super().__init__()

    def _verify(self, command):
        pass

    def _refresh(self):
        pass
