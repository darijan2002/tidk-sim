from Decoder import Decoder
import numpy as np
from HammingCodeCoder import HammingCodeCoder

# Hamming(11,7) decoder
class HammingCodeDecoder(Decoder):

    def decode(self, input_string):
        current_codeword_idx = 0
        codeword_len = 11

        decoded_str = ""

        while current_codeword_idx < len(input_string):
            codeword = input_string[current_codeword_idx:current_codeword_idx + codeword_len]
            cw_vec = [int(x) for x in codeword]

            # print(cw_vec)

            syndrome = {1: 0, 2: 0, 4: 0, 8: 0}
            for i in range(1, codeword_len + 1):
                for mask in [1, 2, 4, 8]:
                    if i & mask and cw_vec[i - 1]:
                        syndrome[mask] = 1 - syndrome[mask]

            row_to_correct = (syndrome[8] << 3) + (syndrome[4] << 2) + (syndrome[2] << 1) + syndrome[1]

            if row_to_correct and row_to_correct<len(input_string):
                cw_vec[row_to_correct - 1] = 1 - cw_vec[row_to_correct - 1]

            print(row_to_correct)

            # error free (probably)

            char = chr(int("".join(str(cw_vec[i - 1]) for i in range(1, 12) if int.bit_count(i) > 1), 2))
            decoded_str += char

            current_codeword_idx += codeword_len

        return decoded_str

    def decode_str_to_binary_vector(self,in_str):
        out_str = self.decode(in_str)



        x = ord(out_str)
        final =  f'{x:07b}'

        out_arr = [int(c) for c in final]

        return out_arr

if __name__ == '__main__':

    coder = HammingCodeCoder()

    #encoded = '00110101100101010100000011100010110011000000111011010010110110010101101011001111110000110010101001110011000000001110010100110110101010101011111001011011110110101011010011000000101110001101010101111111111110000100110000001110101101001101100101111010101010010110000010101100011100110000001010101111111101100110001110001010110110101010011000000101011011001010101000000111000101100110000000010101110010111001001101111110100011111100110011000000111110011001010101111101111001111'
    encoded = coder.encode_string("lmao")
    x = HammingCodeDecoder().decode(encoded)
    print(x)
