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

from abc import ABC, abstractmethod
from typing import List, Tuple

from pi_control_hub_driver_api.device_command import DeviceCommand


class DeviceDriver(ABC):
    """This is the abstract class that needs to be inherited in order to communicate
    with a device."""

    @abstractmethod
    def get_commands(self) -> List[DeviceCommand]:
        """Return the commands that are supported by this device.

        Returns
        -------
        The commands that are supported by this device.
        """
        pass

    def get_command(self, cmd_id: int) -> DeviceCommand:
        """Return the command with the given ID.

        Parameters
        ----------
        cmd_id : int
            The numeric ID of the command.

        Returns
        -------
        The command for the ID or None if the command ID hasn't been found
        """
        result = list(filter(lambda c: c.id == cmd_id, self.get_commands()))
        if result.count() > 0:
            return result[0]
        return None

    @property
    @abstractmethod
    def remote_layout_size(self) -> Tuple[int, int]:
        """
        The size of the remote layout.

        Returns
        -------
        A tuple with the width and height of the layout
        """

    @property
    @abstractmethod
    def remote_layout(self) -> List[List[int]]:
        """
        The layout of the remote.

        Returns
        -------
        The layout as a list of columns.
        """

    @abstractmethod
    def execute(self, command: DeviceCommand):
        """
        Executes the given command.

        Parameters
        ----------
        command : DeviceCommand
            The command that shall be executed
        """

    @property
    @abstractmethod
    def is_device_ready(self) -> bool:
        """
        A flag the determines whether the device is ready.

        Returns
        -------
        true if the device is ready, otherwise false.
        """
