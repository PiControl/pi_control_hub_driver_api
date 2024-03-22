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
from enum import Enum
from typing import List, Tuple
from uuid import UUID

import pluginlib

from pi_control_hub_driver_api.device_driver import DeviceDriver
from pi_control_hub_driver_api.device_info import DeviceInfo


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


@pluginlib.Parent(plugin_type='DeviceDriverDescriptor', group='PiControlHub')
class DeviceDriverDescriptor(ABC):
    """This abstract class is the base for all drivers and must be inherited by
    driver implementations.
    """

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
    @pluginlib.abstractmethod
    def get_devices(self) -> List[DeviceInfo]:
        """Returns a list with the available device instances."""

    @property
    @abstractmethod
    @pluginlib.abstractproperty
    def authentication_method(self) -> AuthenticationMethod:
        """The authentication method that is required when pairing a device."""

    @property
    def requires_authentication(self) -> bool:
        """This flag determines whether an authentication is required when pairing a device."""
        return self.authentication_method != AuthenticationMethod.NONE

    @property
    @abstractmethod
    @pluginlib.abstractproperty
    def requires_pairing(self) -> bool:
        """This flag determines whether pairing is required to communicate with this device."""

    @abstractmethod
    @pluginlib.abstractmethod
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
    @pluginlib.abstractmethod
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
    @pluginlib.abstractmethod
    def create_device_instance(self, device_id: str) -> DeviceDriver:
        """Create a device driver instance for the device with the given ID.

        Parameters
        ----------
        device_id : str
            The ID of the device.

        Returns
        -------
        The instance of the device driver or None in case of an error.
        """
