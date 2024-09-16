#!/usr/bin/env python
from dataclasses import dataclass

# -- Input Message Definition
@dataclass
class InputMsg():
    gACT: int = 0
    gGTO: int = 0
    gSTA: int = 0
    gOBJ: int = 0
    gFLT: int = 0
    gPR: int = 0
    gPO: int = 0
    gCU: int = 0
    
@dataclass
class OutputMsg():
    rACT: int = 0
    rGTO: int = 0
    rATR: int = 0
    rPR: int = 0
    rSP: int = 0
    rFR: int = 0
