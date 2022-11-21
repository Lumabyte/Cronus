import logging
from cronus.core import Cronus
from cronus.lifecycle import Lifecycle

class Service(Lifecycle):
    def __init__(self, cronus: Cronus, name: str) -> None:
        super().__init__()
        self._cronus = cronus
        self._name = name
        self._logger = logging.getLogger(f'service.{self.name}')

    @property
    def cronos(self):
        return self._cronus

    @property
    def name(self):
        return self._name

    @property
    def logger(self):
        return self._logger
