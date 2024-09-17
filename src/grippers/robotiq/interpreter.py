#!/usr/bin/env python
# Software License Agreement (BSD License)
#
# Copyright (c) 2012, Robotiq, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#  * Neither the name of Robotiq, Inc. nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# Copyright (c) 2012, Robotiq, Inc.
# Revision $Id$
# Modifed from the orginal by Dasun Gunasinghe (Adaptation to Generic Class Model)

from base.interpreter import Interpreter 
from grippers.robotiq.msg import InputMsg, OutputMsg

class RobotiqInterpreter(Interpreter):
    def __init__(self):
        super().__init__()
        print(f"[INTERPRETER] Robotiq Type Instantiated")

    def verify(self, command: OutputMsg) -> OutputMsg:
        if not isinstance(command, OutputMsg):
            print(f"[INTERPRETER ERROR] Cannot verify unknown type -> {command}. Expecting type {type(OutputMsg)}")
            return None

        # Verify if each variable is in the correct range
        command.rACT = max(0, command.rACT)
        command.rACT = min(1, command.rACT)

        command.rGTO = max(0, command.rGTO)
        command.rGTO = min(1, command.rGTO)

        command.rATR = max(0, command.rATR)
        command.rATR = min(1, command.rATR)

        command.rPR  = max(0,   command.rPR)
        command.rPR  = min(255, command.rPR)    

        command.rSP  = max(0,   command.rSP)
        command.rSP  = min(255, command.rSP)    

        command.rFR  = max(0,   command.rFR)
        command.rFR  = min(255, command.rFR) 

        # Return the verified command
        return command 

    def refresh(self, command: OutputMsg) -> list:
        if not isinstance(command, OutputMsg):
            print(f"[INTERPRETER ERROR] Cannot refresh command as it is incorrect type {type(command)}")
            return []

        # Limit the value of each variable
        command = self.verify(command)

        # Create message list from verified command
        message: list = []
        message.append(command.rACT + (command.rGTO << 3) + (command.rATR << 4))
        message.append(0)
        message.append(0)
        message.append(command.rPR)
        message.append(command.rSP)
        message.append(command.rFR)  

        return message

    def interpret(self, value: list = []) -> InputMsg:
        message = InputMsg()
        if value is None or value == list():
            print(f"[INTERPRETER ERROR] Client Message is Empty")
            return message

        message.gACT = (value[0] >> 0) & 0x01
        message.gGTO = (value[0] >> 3) & 0x01
        message.gSTA = (value[0] >> 4) & 0x03
        message.gOBJ = (value[0] >> 6) & 0x03
        message.gFLT =  value[2]
        message.gPR  =  value[3]
        message.gPO  =  value[4]
        message.gCU  =  value[5]

        return message

    def generate(self, value) -> list:
        # The following is existing functionality
        command = OutputMsg()
        if value == 'a':
            command.rACT = 1
            command.rGTO = 1
            command.rSP  = 255
            command.rFR  = 150
        elif value == 'r':
            command.rACT = 0

        if value == 'c':
            command.rPR = 255

        if value == 'o':
            command.rPR = 0   

        #If the command entered is a int, assign this value to rPRA
        if isinstance(value, int):
            command.rPR = int(value)
            # Clamping behaviour
            if command.rPR > 255:
                command.rPR = 255
            if command.rPR < 0:
                command.rPR = 0
            
        if value == 'f':
            command.rSP += 25
            if command.rSP > 255:
                command.rSP = 255
                
        if value == 'l':
            command.rSP -= 25
            if command.rSP < 0:
                command.rSP = 0

        if value == 'i':
            command.rFR += 25
            if command.rFR > 255:
                command.rFR = 255
                
        if value == 'd':
            command.rFR -= 25
            if command.rFR < 0:
                command.rFR = 0

        output = self.refresh(command)
        return output


