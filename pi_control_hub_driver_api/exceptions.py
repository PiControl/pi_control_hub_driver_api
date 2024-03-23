"""
   Copyright 2024 Thomas Bonk

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

from pi_control_hub_driver_api.device_command import DeviceCommand
from pi_control_hub_driver_api.device_driver import DeviceDriver


class DeviceDriverException(Exception):
    """This is the base exception class for all device driver
    related exceütions.
    """

    def __init__(self, message: str, cause: Exception = None):
        self._message = message
        self._cause = cause

    def __str__(self) -> str:
        return self._message

class CommandNotFoundException(DeviceDriverException):
    """This exception is thrown if a command is not found."""

    def __init__(self, device_driver: DeviceDriver, command_id: int):
        DeviceDriverException.__init__(self, f"The device '{device_driver.name}' (id = {device_driver.device_id}) has no command with id '{command_id}'")

class DeviceCommandException(DeviceDriverException):
    """This exception is thrown if an error occurs during command execution."""

    def __init__(self, command: DeviceCommand, device_driver: DeviceDriver = None):
        if device_driver:
            DeviceDriverException.__init__(self, f"Error while executing the command '{command.title}' (id = {command.id}) for device '{device_driver.name}' (id = {device_driver.device_id}).")
        else:
            DeviceDriverException.__init__(self, f"Error while executing the command '{command.title}' (id = {command.id}).")
