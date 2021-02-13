from abc import ABC, abstractmethod
from argparse import Namespace

from openrazer.client import DeviceManager


class Setter(ABC):

    def __init__(self, device_manager: DeviceManager, args: Namespace):
        self.device_manager = device_manager
        self.args = args

    @abstractmethod
    def set(self, **kwargs):
        ...
