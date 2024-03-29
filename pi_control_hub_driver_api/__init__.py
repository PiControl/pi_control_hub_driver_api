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

__version__ = '0.0.1'
__author__ = 'Thomas Bonk'
__author_email__ = 'thomas@meandmymac.de'

from abc import ABC, abstractmethod, abstractproperty
from enum import Enum
from typing import List, Tuple
from uuid import UUID

import pkg_resources


class DeviceCommand(ABC):
    """This abstract class is the base for all commands of a device. Inherit
    this class and implement the `execute` method in your implementation.
    """

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
        """
        Execute the command. This method must be implemented by the specific command.

        Raises
        ------
        `DeviceCommandException` in case of an error while executing the command.
        """


class DeviceInfo(object):
    """This class is used to provide information for a device. It can be inherited."""

    def __init__(self, name: str, device_id: str):
        self._name = name
        self._id = device_id

    @property
    def name(self) -> str:
        """The device name."""
        return self._name

    @property
    def device_id(self) -> str:
        """The device ID."""
        return self._id


class DeviceDriver(ABC):
    """This is the abstract class that needs to be inherited in order to communicate
    with a device."""

    def __init__(self, device_info: DeviceInfo):
        self._device_info = device_info

    @property
    def name(self) -> str:
        """The device name."""
        return self._device_info.name

    @property
    def device_id(self) -> str:
        """The device ID."""
        return self._device_info.device_id

    @abstractmethod
    def get_commands(self) -> List[DeviceCommand]:
        """Return the commands that are supported by this device.

        Returns
        -------
        The commands that are supported by this device.

        Raises
        ------
        `DeviceDriverException` in case of an error.
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
        The command for the ID.

        Raises
        ------
        `CommandNotFoundException` if the command is not known.

        `DeviceDriverException` in case of an other error.
        """
        result = list(filter(lambda c: c.id == cmd_id, self.get_commands()))
        if result.count() > 0:
            return result[0]
        raise CommandNotFoundException(self.name, cmd_id)

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

        Raises
        ------
        `DeviceCommandException` in case of an error while executing the command.
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


class AuthenticationMethod(Enum):
    """Definition of the different authentication types."""
    NONE = 0
    """No authentication required"""

    PIN = 1
    """Authenticate with a PIN"""

    PASSWORD = 2
    """Authenticate with a password"""

    USER_AND_PASSWORD = 3
    """Authenticate with a username and password"""


class DeviceDriverDescriptor(ABC):
    """This abstract class is the base for all drivers and must be inherited by
    driver implementations.
    """

    _config_path = None

    @staticmethod
    def set_config_path(config_path: str):
        """The PiControl Hub server sets the config path where device drivers can
        store and read their configurations."""
        DeviceDriverDescriptor._config_path = config_path

    @staticmethod
    def get_config_path() -> str:
        """The config path where device drivers can store and read their configurations."""
        return DeviceDriverDescriptor._config_path

    def __init__(self, driver_id: UUID, display_name: str, description: str):
        self._driver_id = driver_id
        self._display_name = display_name
        self._description = description

    @property
    def driver_id(self) -> UUID:
        """The driver ID."""
        return self._driver_id

    @property
    def display_name(self) -> str:
        """The display name of the device descriptor."""
        return self._display_name

    @property
    def description(self) -> str:
        """The description of the device descriptor."""
        return self._description

    @abstractmethod
    def get_devices(self) -> List[DeviceInfo]:
        """Returns a list with the available device instances."""

    @property
    @abstractproperty
    def authentication_method(self) -> AuthenticationMethod:
        """The authentication method that is required when pairing a device."""

    @property
    def requires_authentication(self) -> bool:
        """This flag determines whether an authentication is required when pairing a device."""
        return self.authentication_method != AuthenticationMethod.NONE

    @property
    @abstractproperty
    def requires_pairing(self) -> bool:
        """This flag determines whether pairing is required to communicate with this device."""

    @abstractmethod
    def start_pairing(self, device_info: DeviceInfo, remote_name: str) -> Tuple[str, bool]:
        """Start the pairing process with the given device.

        Parameters
        ----------
        device_info : DeviceInfo
            The device to pair with.
        remote_name : str
            The name of the remote that will control this device.

        Returns
        -------
        A tuple consisting of a pairing request ID and a flag that determines whether the device
        provides a PIN.
        """

    @abstractmethod
    def finalize_pairing(self, pairing_request: str, credentials: str, device_provides_pin: bool) -> bool:
        """Finalize the pairing process

        Parameters
        ----------
        pairing_request : str
            The pairing request ID returns by ``start_pairing``
        device_provides_pin : bool
            The flag that determines whether the device provides a PIN.
        """

    @abstractmethod
    def create_device_instance(self, device_id: str) -> DeviceDriver:
        """Create a device driver instance for the device with the given ID.

        Parameters
        ----------
        device_id : str
            The ID of the device.

        Returns
        -------
        The instance of the device driver or None in case of an error.

        Raises
        ------
        `DeviceNotFoundException` if the device hasn't been found.
        """



class DeviceDriverException(Exception):
    """This is the base exception class for all device driver
    related exceütions.
    """

    def __init__(self, message: str, cause: Exception = None):
        self._message = message
        self._cause = cause

    def __str__(self) -> str:
        return self._message

class DeviceNotFoundException(DeviceDriverException):
    """This exception is thrown, if a device wasn't found."""
    def __init__(self, device_id: str):
        DeviceDriverException.__init__(self, f"Device with ID '{device_id}' not found.")

class CommandNotFoundException(DeviceDriverException):
    """This exception is thrown if a command is not found."""

    def __init__(self, device_driver_name: str, command_id: int):
        DeviceDriverException.__init__(self, f"The device '{device_driver_name}' has no command with id '{command_id}'")

class DeviceCommandException(DeviceDriverException):
    """This exception is thrown if an error occurs during command execution."""

    def __init__(self, command: DeviceCommand, device_driver_name: str = None):
        if device_driver_name:
            DeviceDriverException.__init__(self, f"Error while executing the command '{command.title}' (id = {command.id}) for device '{device_driver_name}'.")
        else:
            DeviceDriverException.__init__(self, f"Error while executing the command '{command.title}' (id = {command.id}).")


def installed_drivers(driver_name_prefix: str = 'pi-control-hub-driver-') -> List[DeviceDriverDescriptor]:
    """This function returns a list of names of installed PiControl drivers.

    Parameters
    ----------
    `driver_name_prefix`: `str`
        Prefix of the package names of drivers packages.

    Returns
    -------
    `List[DeviceDriverDescriptor]`: List of installed PiControl Hub drivers"""

    driver_descriptors = []
    for package in pkg_resources.working_set:
        if package.key.startswith(driver_name_prefix) and not package.key == 'pi-control-hub-driver-api':
            entry_map = package.get_entry_map()
            entry_point_meta = entry_map["pi_control_hub_driver"]["driver_descriptor"]
            entry_point = entry_point_meta.load()
            driver_descriptors.append(entry_point())
    return driver_descriptors
