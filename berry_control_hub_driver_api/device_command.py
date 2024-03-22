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


class DeviceCommand(ABC):
    """This abstract class is the base for all commands of a device. Inherit
    this class and implement the `execute` method in your implementation.
    """
    _id: int
    _title: str
    _icon: bytes

    def __init__(self, cmd_id: int, title: str, icon: bytes):
        """Creates a device command with the given data.

        Paramters
        ---------
        id : int
            Command ID
        title : str
            Title of the command
        icon : bytes
            Icon for the command that can be rendered by a UI
        """
        self._id = cmd_id
        self._title = title
        self._icon = icon

    @property
    def id(self) -> int:
        """Getter for the command ID."""
        return self._id

    @property
    def title(self) -> str:
        """Getter for the command title."""
        return self._title

    @property
    def icon(self) -> bytes:
        """Getter for the command icon."""
        return self._icon

    @abstractmethod
    def execute(self):
        """Execute the command. This method must be implemented by the specific command."""
