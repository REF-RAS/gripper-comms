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
from robotiq.msg import InputMsg, OutputMsg

class RobotiqInterpreter(Interpreter):
    def __init__(self):
        super().__init__()

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

    def refresh(self, command: OutputMsg) -> OutputMsg:
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
