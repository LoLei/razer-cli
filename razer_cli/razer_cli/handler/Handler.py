from abc import ABC, abstractmethod
from argparse import Namespace

from openrazer.client import DeviceManager


class Handler(ABC):

    def __init__(self, device_manager: DeviceManager, args: Namespace, version: str = None):
        self.device_manager = device_manager
        self.args = args
        self.version = version

    @abstractmethod
    def handle(self):
        ...
