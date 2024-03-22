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

from setuptools import setup

from berry_control_hub_driver_api import __version__, __author__, __author_email__

setup(
    name='berry_control_hub_driver_api',
    version=__version__,
    description='Base API that must be implemented by BerryControl Hub drivers',
    url='https://github.com/BerryControl/berry_control_hub_driver_api',
    author=__author__,
    author_email=__author_email__,
    license='Apache 2.0',
    packages=['berry_control_hub_driver_api'],
    install_requires=[
        'pluginlib>=0.9.1',
    ],

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3',
    ],
)
