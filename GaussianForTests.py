import numpy as np


class GaussianForTests:
    @staticmethod
    def convert_to_symbols(vector):
        return np.add(np.multiply(vector, 2), -1)

    def __init__(self, noise_dB):
        self.scale = 1.0 / (10.0**(noise_dB / 20.0))

    def transmit_sequence(self, vector):
        noise = np.random.normal(0, 1, len(vector))
        noise = np.multiply(noise, self.scale)
        return np.add(vector, noise)