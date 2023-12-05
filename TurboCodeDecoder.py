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

    def reset(self):
        self.LLR_ext = [0.0 for _ in range(self.block_size + self.tail_bits)]
        self.first_decoder = SISODecoder()
        self.second_decoder = SISODecoder()


    def interleave(self,input):
        interleaved = [0 for _ in range(self.block_size + self.tail_bits)]
        for  i in range(self.block_size):
            interleaved[i] = input[self.interleaver[i]]
        return interleaved

    def deinterleave(self,input):
        deinterleaved = [0 for _ in range(self.block_size+self.tail_bits)]
        for i in range(self.block_size):
            deinterleaved[self.interleaver[i]] = input[i]
        return deinterleaved

    def bit_predictions(self,input):
        input_tuples = [ x for x in zip(input[::3], input[1::3], self.LLR_ext,strict=True)]

        # Here we get predictions from first decoder, input is LLR_ext(initially 0)
        # and input values from the channel for the un-interleaved data

        LLR_from_first = self.first_decoder.decode(input_tuples)
        for i in range(len(LLR_from_first)):
            LLR_from_first[i] = LLR_from_first[i] - self.LLR_ext[i] - 2 * input[::3][i]

        # Below we interleave data and input it into the second decoder together with the
        # interleaved RSC and the extrinsic vector from the first decoder
        input_interleaved = self.interleave(input[::3])
        LLR_interleaved = self.interleave(LLR_from_first)
        input_tuples = [x for x in zip(input_interleaved, input[2::3], LLR_interleaved,strict=True)]

        LLR_from_second = self.second_decoder.decode(input_tuples)
        for i in range(len(LLR_from_first)):
            LLR_from_first[i] = LLR_from_second[i] - LLR_interleaved[i] - 2 * input_interleaved[i]

        # Here we set the extrinsic values to the de-interleaved output of the second decoder
        # we do this in order to use them in the next iteration as the input into the first decoder
        self.LLR_ext = self.deinterleave(LLR_from_second)

        # We check if predictions are the same, we stop here because further iteration
        # will have no effect on the predictions
        pred_1 = [int(s > 0) for s in LLR_from_first]
        pred_2 = [int(s > 0) for s in self.LLR_ext]
        return pred_1 == pred_2

    def decode(self,input_array):
        for iteration in range(self.max_iter):
            if self.bit_predictions(input_array):
                break
        bit_array = [str(int(val >= 0)) for val in self.LLR_ext]
        return "".join(bit_array)

    def decode_sequence(self,sequence):
        output = []
        for start_index in range(0,len(sequence),27):
            print(sequence[start_index:start_index+27])
            output.append( self.decode(sequence[start_index:start_index+27])[:-2])
            print(chr(int(self.decode(sequence[start_index:start_index+27])[:-2],base=2)))
            self.reset()
        return output


