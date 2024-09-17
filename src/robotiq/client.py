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
# Modifed from the orginal comModbusTcp by Dasun Gunasinghe (Adaptation to Generic Class Model)

from base.client import Client
from pymodbus.client import ModbusSerialClient
from pymodbus import ModbusException
from math import ceil

class RobotiqClient(Client):
    def __init__(self):
        """Robotiq Client Initialiser
        """
        super().__init__()
        print(f"[CLIENT] Robotiq Type Instantiated")
        # TODO: config read in to get these params
        self._client = ModbusSerialClient(
            method='rtu',
            port='COM4',
            stopbits=1,
            bytesize=8,
            baudrate=115200,
            timeout=0.5
        )

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

    def status(self, num_bytes: int = 0) -> list:
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
        output: list = []
        for i in range(0, num_regs) :
            output.append((resp.getRegister(i) & 0xFF00) >> 8)
            output.append(resp.getRegister(i) & 0xFF00)

        # Output the result
        return output
