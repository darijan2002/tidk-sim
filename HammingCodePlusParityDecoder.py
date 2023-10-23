from Decoder import Decoder
import numpy as np


# TODO: add extra parity bit
# Hamming(11,7) with extra parity bit coder
class HammingCodePlusParityDecoder(Decoder):
    _generating_matrix = [[1, 1, 0, 1, 1, 0, 1],
                          [1, 0, 1, 1, 0, 1, 1],
                          [0, 1, 1, 1, 0, 0, 0],
                          [0, 0, 0, 0, 1, 1, 1],
                          [1, 0, 0, 0, 0, 0, 0],
                          [0, 1, 0, 0, 0, 0, 0],
                          [0, 0, 1, 0, 0, 0, 0],
                          [0, 0, 0, 1, 0, 0, 0],
                          [0, 0, 0, 0, 1, 0, 0],
                          [0, 0, 0, 0, 0, 1, 0],
                          [0, 0, 0, 0, 0, 0, 1]]

    _parity_check_matrix = [[1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
                            [0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
                            [0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1],
                            [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1]]

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

            if row_to_correct:
                cw_vec[row_to_correct - 1] = 1 - cw_vec[row_to_correct - 1]

            print(row_to_correct)

            # error free (probably)

            char = chr(int("".join(str(cw_vec[i - 1]) for i in range(1, 12) if int.bit_count(i) > 1), 2))
            decoded_str += char

            current_codeword_idx += codeword_len

        return decoded_str


if __name__ == '__main__':
    encoded = '11011111010111110011000110110101010111001001111011001101010101111110011000000010111110101010011011010001011001'
    x = HammingCodePlusParityDecoder().decode(encoded)
    print(x)
