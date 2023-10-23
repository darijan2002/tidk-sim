from Decoder import Decoder
import numpy as np
class HammingCodeDecoder(Decoder):
    generating_matrix =  [[1,1,0,1,1,0,1],
                          [1,0,1,1,0,1,1],
                          [0,1,1,1,0,0,0],
                          [0,0,0,0,1,1,1],
                          [1,0,0,0,0,0,0],
                          [0,1,0,0,0,0,0],
                          [0,0,1,0,0,0,0],
                          [0,0,0,1,0,0,0],
                          [0,0,0,0,1,0,0],
                          [0,0,0,0,0,1,0],
                          [0,0,0,0,0,0,1]]

    parity_check_matrix = [[1,0,1,0,1,0,1,0,1,0,1],
                           [0,1,1,0,0,1,1,0,0,1,1],
                           [0,0,0,1,1,1,1,0,0,0,0],
                           [0,0,0,0,0,0,0,1,1,1,1]]
    def decode(self,input_string):




