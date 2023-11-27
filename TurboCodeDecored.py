from Decoder import Decoder
import numpy as np
from SISODecoder import SISODecoder

# Turbo code decoder
class TurboCodeDecoder(Decoder):

    def __init__(self,interleaver,max_iter):
        self.interleaver = interleaver
        self.block_size = 7
        self.tail_bits = 2
        self.max_iter = max_iter
        self.decoders = 2 * [SISODecoder()]
        self.LLR_ext = [0.0 for _ in range(self.block_size + self.tail_bits)]

    def interleave(self,input):
        interleaved = [input[i] for i in self.interleaver]
        return interleaved

    def deinterleave(self,input):
        deinterleaved = [0 for _ in range(self.block_size)]
        for i in range(self.block_size):
            deinterleaved[i] = input[self.interleaver[i]]

    def bit_predictions(self):
        input_

