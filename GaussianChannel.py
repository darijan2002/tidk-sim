import math
import numpy as np


class GaussianChannel:
    channel_power = 1
    variance = 1

    def __init__(self, channel_power, variance):
        self.channel_power = channel_power
        self.variance = variance

    def transmit_bit(self, bit):
        sign = 1

        if bit == '0':
            sign = -1

        mean = sign * math.sqrt(self.channel_power)
        return mean + np.random.normal(0, math.sqrt(self.variance))

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
            output_bits += str(self.recieve_signal(signal))

        return int(output_bits, 2)
