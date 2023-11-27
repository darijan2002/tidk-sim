from abc import ABC, abstractmethod


class Decoder(ABC):
    @abstractmethod
    def decode(self, input_string):
        pass
