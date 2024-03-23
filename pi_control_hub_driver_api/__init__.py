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

__version__ = '0.2.1'
__author__ = 'Thomas Bonk'
__author_email__ = 'thomas@meandmymac.de'

import importlib
from typing import List

import pkg_resources

from pi_control_hub_driver_api.device_driver_descriptor import DeviceDriverDescriptor
from pi_control_hub_driver_api.exceptions import DeviceDriverException


def installed_drivers(driver_name_prefix: str = 'pi_control_hub_driver_') -> List[str]:
    """This function returns a list of names of installed PiControl drivers.

    Parameters
    ----------
    `driver_name_prefix`: `str`
        Prefix of the package names of drivers packages.

    Returns
    -------
    `List[str]`: List of names of installed PiControl Hub drivers"""

    installed_packages = []
    for package in pkg_resources.working_set:
        if package.key.startswith(driver_name_prefix):
            installed_packages.append(package.key)
    return installed_packages

def load_driver(driver_name: str) -> DeviceDriverDescriptor:
    """Loads the driver with the given name.

    Parameters
    ----------
    `driver_name`: `str``
        The of the driver to load.

    Returns
    -------
    `DeviceDriverDescriptor`: The instance of the driver descriptor.

    Raises
    ------
    `DeviceDriverException`: If an error occured.
    """
    try:
        # Dynamically import the package
        package_module = importlib.import_module(driver_name)

        # Get the function that returns the driver descriptor instance
        function = getattr(package_module, 'get_driver_descriptor')

        return function()
    except ImportError as exc:
        raise DeviceDriverException(
                f"Driver '{driver_name}' not found.",
                cause=exc,
            ) from exc
    except AttributeError as exc:
        raise DeviceDriverException(
                f"Function 'get_driver_descriptor' not found in driver '{driver_name}'.",
                cause=exc,
            ) from exc
