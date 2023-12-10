from Coder import Coder
import numpy as np

from RSC import RSC


# Turbo code coder
class TurboCodeCoder(Coder):
    interleaver = []

    def __init__(self,interleaver):
        self.interleaver = interleaver

    def encode_bits(self,bit_vector):
        output = []
        rsc1, rsc2 = RSC(), RSC()
        bit_vector_i = [0 for _ in range(len(bit_vector))]

        for i in range(len(bit_vector)):
            bit_vector_i[i] = bit_vector[self.interleaver[i]]

        for b in range(len(bit_vector)):
            output.append(bit_vector[b])
            output.append(rsc1.push(bit_vector[b]))
            output.append(rsc2.push(bit_vector_i[b]))

        terminated_rsc_1 = [rsc1.terminate() for _ in range(2)]
        terminated_rsc_2 = [rsc2.terminate() for _ in range(2)]

        for x,y in zip(terminated_rsc_1, terminated_rsc_2):
            output.append(x)
            output.append(x)
            output.append(y)

        print()
        return output
    def encode_string(self, string):
        # print(f'INTERLEAVER: {self.interleaver}')

        output = []
        rsc1, rsc2 = RSC(), RSC()
        for c in string:
            output.append("")

            to_bin = f'{ord(c):07b}'
            to_bin_i = [''] * len(to_bin)
            for i in range(len(to_bin)):
                to_bin_i[i] = to_bin[self.interleaver[i]]

            for b in range(len(to_bin)):
                output[-1] += to_bin[b]
                output[-1] += str(rsc1.push(int(to_bin[b])))
                output[-1] += str(rsc2.push(int(to_bin_i[b])))

            terminated_rsc_1 = [rsc1.terminate() for _ in range(2)]
            terminated_rsc_2 = [rsc2.terminate() for _ in range(2)]


            output[-1] += "".join([ f'{x}{x}{y}' for x,y in zip(terminated_rsc_1,terminated_rsc_2)])

        return "".join(output)


if __name__ == '__main__':
    s = 'T'
    x = TurboCodeCoder([0,1,2,3,4,5,6]).encode_string(s)
    print(x)
