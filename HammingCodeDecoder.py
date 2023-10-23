from Decoder import Decoder
import numpy as np


class HammingCodeDecoder(Decoder):
    generating_matrix = [[1, 1, 0, 1, 1, 0, 1],
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

    parity_check_matrix = [[1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
                           [0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1],
                           [0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1]]

    def decode(self, input_string):
        current_codeword_idx = 0
        codeword_len = 11

        decoded_str = ""

        while current_codeword_idx < len(input_string):
            codeword = input_string[current_codeword_idx:current_codeword_idx + codeword_len]
            cw_vec = [int(x) for x in codeword]

            # print(cw_vec)

            res = np.matmul(self.parity_check_matrix, cw_vec)
            res = [x & 1 for x in res]

            row_to_correct = int("".join([str(x) for x in res]), 2)

            # print(row_to_correct)
            if row_to_correct:
                cw_vec[row_to_correct] = 1-cw_vec[row_to_correct]

            # error free (probably)

            char = chr(int("".join(str(cw_vec[i-1]) for i in range(1, 12) if int.bit_count(i) > 1), 2))
            decoded_str += char

            current_codeword_idx += codeword_len

        return decoded_str


# if __name__ == '__main__':
#     encoded = '10111111010111110011000110110101010111001001111011001101010101111110011000000010111110101010011011010001011001'
#     x = HammingCodeDecoder().decode(encoded)
#     print(x)