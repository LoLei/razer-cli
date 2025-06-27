from abc import ABC, abstractmethod
from argparse import Namespace

from openrazer.client import DeviceManager

from typing import Optional
from razer_cli.razer_cli.setter.setter import Setter


class Handler(ABC):
    def __init__(self, device_manager: DeviceManager, args: Namespace, version: Optional[str] = None, setter: Optional[Setter] = None):
        self.device_manager = device_manager
        self.args = args
        self.version = version
        self.setter = setter

    @abstractmethod
    def handle(self):
        ...
