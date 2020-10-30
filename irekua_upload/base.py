from abc import ABC
from abc import abstractmethod


class IrekuaOperation(ABC):
    @abstractmethod
    def run(self, *args, **kwargs):
        pass
