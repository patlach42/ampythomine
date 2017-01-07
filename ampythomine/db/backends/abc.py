from abc import abstractmethod
from ampythomine.patterns import Singleton


class DatabaseBackend(metaclass=Singleton):
    @abstractmethod
    def init(self, config):
        pass
