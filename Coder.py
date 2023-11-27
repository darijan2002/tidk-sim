from abc import ABC, abstractmethod


class Coder(ABC):
    @abstractmethod
    def encode_string(self, string):
        pass
