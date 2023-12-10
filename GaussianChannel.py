import math
import numpy as np


class GaussianChannel:
    stddev = 1

    def __init__(self, noise_dB):
        self.stddev = (10 ** (noise_dB / 20)) ** (-1)

    def transmit_sequence(self, sequence):

        output = []
        for each in sequence:
            output.append(self.transmit_bit(each))
        return output

    def transmit_bit(self, bit):
        sign = 1 if bit == '1' else -1

        return sign + np.random.normal(0, self.stddev)

    def receive_signal(self, signal):
        if signal >= 0:
            return 1
        else:
            return 0

    def transfer_integer(self, hex_number):
        binary = bin(hex_number)
        binary = binary[2:]

        signal_list = list()

        for bit in binary:
            signal_list.append(self.transmit_bit(bit))

        output_bits = ""

        for signal in signal_list:
            output_bits += str(self.receive_signal(signal))

        return int(output_bits, 2)
