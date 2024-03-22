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
