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
#
# Modifed from the orginal comModbusTcp by Kelsey Hawkins @ Georgia Tech
# Modifed from the orginal by Dasun Gunasinghe (Adaptation to Generic Class Model)

from base.client import Client, Interpreter
from pymodbus.client import ModbusSerialClient
from pymodbus import ModbusException
from dataclasses import dataclass
from math import ceil

# -- Message Definition
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

# --- Client Definition
class RobotiqModbusSerialClient(Client):
    def __init__(self, interpreter: Interpreter):
        """Robotiq Client Initialiser
        """
        super().__init__(interpreter=interpreter)
        print(f"[CLIENT] Robotiq ModbusSerialClient Type Instantiated")
        # TODO: config read in to get these params
        self._client = ModbusSerialClient(
            framer='rtu',
            port='COM4',
            stopbits=1,
            bytesize=8,
            baudrate=115200,
            timeout=0.5,        
        )

    def setup(self) -> bool:
        """Conducts required setup for the client
        """
        # Send the required initialise params
        print(f"[CLIENT] Setup Procedure Starting...")
        if not self.send(self._interpreter.generate_output('r')):
            print(f"[CLIENT ERROR] Setup Procedure Failed to Send [r]")
            return False

        # TODO: Timeout needed?
        time.sleep(1)
    
        if not self.send(self._interpreter.generate_output('a')):
            print(f"[CLIENT ERROR] Setup Procedure Failed to Send [a]")
            return False

        # TODO: Timeout needed?
        time.sleep(1)
        print(f"[CLIENT] Setup Procedure Completed")
        return True

    def connect(self) -> bool:
        self._connected = self._client.connect()
        print(f"[CLIENT CONNECTION] Status is {self._connected}")
        return self._connected

    def disconnect(self):
        if not self._connected:
            print(f"[CLIENT ERROR] Cannot disconnect as not connected")
            return

        self._client.close()
        self._connected = False

    def send(self, command) -> bool:
        if command is None:
            print(f"[CLIENT ERROR] Cannot Send as command is None")
            return False

        if not self._connected:
            print(f"[CLIENT ERROR] Cannot Send as Client is Not Connected")
            return False

        if len(command) % 2 == 1:
            command.append(0)
        
        # Initiate message and fill by combining two bytes in one register
        message: list = []
        for i in range(0, int(len(command)/2)):
            message.append((command[2*i] << 8) + command[2*i+1])

        try:
            # NOTE: value is the value to write
            # NOTE: slave is the Modbus Slave ID
            self._client.write_registers(
                address=0x03E8, 
                values=message, 
                slave=9
            )
            return True
        except ModbusException as e:
            print(f"[CLIENT ERROR] ModbusException on Send -> {e}")
            self._connected = False
            return False

    def get_status(self, num_bytes: int = 6) -> list:
        """Gets the status from a connected Robotiq Gripper 
        """
        if num_bytes is None or num_bytes <= 0:
            print(f"[CLIENT ERROR] Cannot get status as num_bytes is invalid -> {num_bytes}")
            return [] 
            
        if not self._connected:
            print(f"[CLIENT ERROR] Cannot get status as Client is Not Connected")
            return [] 

        num_regs: int = int(ceil(num_bytes/2.0))

        # Get the status from the device
        resp = None
        try:
            # NOTE: count is the number of coils to read
            # NOTE: slave is the Modbus Slave ID
            resp = self._client.read_holding_registers(
                address=0x07D0,
                count=num_regs,
                slave=9
            )
        except ModbusException as e:
            print(f"[CLIENT ERROR] ModbusException on Status Read -> {e}")
            self._connected = False
            return list()

        # Setup output and fill with bytes in correct order
        # Two byte extraction
        print(f"[CLIENT] GOT: {resp}")
        output: list = []
        for i in range(0, num_regs) :
            output.append((resp.getRegister(i) & 0xFF00) >> 8)
            output.append(resp.getRegister(i) & 0xFF00)
        # Output the result
        return output

# --- Interpreter Definition
class RobotiqInterpreter(Interpreter):
    def __init__(self):
        super().__init__()
        print(f"[INTERPRETER] Robotiq Type Instantiated")
        self._command: OutputMsg = OutputMsg()

    def verify_output(self, command: OutputMsg) -> OutputMsg:
        """Confirms if the output message is within required bounds
        """
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

    def refresh_output(self, command: OutputMsg) -> list:
        """Refreshes/prepares output message into required type for sending 
        """
        if not isinstance(command, OutputMsg):
            print(f"[INTERPRETER ERROR] Cannot refresh command as it is incorrect type {type(command)}")
            return []

        # Limit the value of each variable
        command = self.verify_output(command)

        # Create message list from verified command
        message: list = []
        message.append(command.rACT + (command.rGTO << 3) + (command.rATR << 4))
        message.append(0)
        message.append(0)
        message.append(command.rPR)
        message.append(command.rSP)
        message.append(command.rFR)  

        return message

    def interpret_input(self, value: list = []) -> InputMsg:
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

    def generate_output(self, value: str) -> list:
        # The following is existing functionality
        if value == 'a':
            self._command.rACT = 1
            self._command.rGTO = 1
            self._command.rSP  = 255
            self._command.rFR  = 150
        elif value == 'r':
            self._command.rACT = 0

        if value == 'c':
            self._command.rPR = 255

        if value == 'o':
            self._command.rPR = 0   

        #If the command entered is a int, assign this value to rPRA
        if value.isnumeric():
            self._command.rPR = int(value)
            # Clamping behaviour
            if self._command.rPR > 255:
                self._command.rPR = 255
            if self._command.rPR < 0:
                self._command.rPR = 0
            
        if value == 'f':
            self._command.rSP += 25
            if self._command.rSP > 255:
                self._command.rSP = 255
                
        if value == 'l':
            self._command.rSP -= 25
            if self._command.rSP < 0:
                self._command.rSP = 0

        if value == 'i':
            self._command.rFR += 25
            if self._command.rFR > 255:
                self._command.rFR = 255
                
        if value == 'd':
            self._command.rFR -= 25
            if self._command.rFR < 0:
                self._command.rFR = 0

        output = self.refresh_output(self._command)
        print(f"[CLIENT] Generated Output: {output} | value: {value}")
        return output


