import logging
from cronus.lifecycle import Lifecycle

class Source(Lifecycle):
    def __init__(self, name: str) -> None:
        super().__init__()
        self._name = name
        self._logger = logging.getLogger(f'source.{self.name}')

    @property
    def name(self):
        return self._name

    @property
    def logger(self):
        return self._logger
