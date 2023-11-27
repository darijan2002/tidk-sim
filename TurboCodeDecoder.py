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
        self.first_decoder = SISODecoder()
        self.second_decoder = SISODecoder()
        self.LLR_ext = [0.0 for _ in range(self.block_size + self.tail_bits)]

    def interleave(self,input):
        interleaved = [input[i] for i in self.interleaver]
        return interleaved

    def deinterleave(self,input):
        deinterleaved = [0 for _ in range(self.block_size)]
        for i in range(self.block_size):
            deinterleaved[i] = input[self.interleaver[i]]

    def bit_predictions(self,input):
        input_tuples = list(zip(input[::3], input[1::3], self.LLR_ext))

        LLR_from_first = self.first_decoder.decode(input_tuples)

        for i in range(len(LLR_from_first)):
            LLR_from_first[i] = LLR_from_first[i] - self.LLR_ext[i] - 2 * input[::3][i]

        input_interleaved = self.interleave(input[::3])
        LLR_interleaved = self.interleave(LLR_from_first)

        input_tuples = list(zip(input_interleaved, input[2::3], self.LLR_ext))

        LLR_from_second = self.second_decoder.decode(input_tuples)

        self.LLR_ext = self.deinterleave(LLR_from_second)

        pred_1 = [int(s > 0) for s in LLR_from_first]
        pred_2 = [int(s > 0) for s in LLR_from_second]
        return pred_1 == pred_2



    def decode(self,input_string):
        input_array = [int(x) for x in input_string]

        for iter in range(self.max_iter):
            if self.bit_predictions(input_array):
                break

        bit_array = [int(val >= 0) for val in self.LLR_ext]

        return bit_array

