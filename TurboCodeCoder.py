from Coder import Coder
import numpy as np

from RSC import RSC


# Turbo code coder
class TurboCodeCoder(Coder):
    interleaver = []

    def __init__(self,interleaver):
        self.interleaver = interleaver

    def encode_string(self, string):
        print(f'INTERLEAVER: {self.interleaver}')

        output = []
        for c in string:
            rcs1, rcs2 = RSC(), RSC()
            output.append("")
            to_bin = f'{ord(c):07b}'
            to_bin_i = [''] * 7
            for i in range(7):
                to_bin_i[self.interleaver[i]] = to_bin[i]

            for b in range(len(to_bin)):
                output[-1] += to_bin[b]
                output[-1] += str(rcs1.push(int(to_bin[b])))
                output[-1] += str(rcs2.push(int(to_bin_i[b])))

            terminated_rcs_1 = [rcs1.terminate() for _ in range(2)]
            terminated_rcs_2 = [rcs2.terminate() for _ in range(2)]
            print(terminated_rcs_1)
            print(terminated_rcs_2)

            output[-1] += "".join([ f'{x}{x}{y}' for x,y in zip(terminated_rcs_1,terminated_rcs_2)])

            print(to_bin)
            print(to_bin_i)
            print("-" * 10)

        return "".join(output)


if __name__ == '__main__':
    s = 'T'
    x = TurboCodeCoder([0,1,2,3,4,5,6]).encode_string(s)
    print(x)
