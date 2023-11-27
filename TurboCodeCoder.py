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
            print(terminated_rsc_1)
            print(terminated_rsc_2)

            output[-1] += "".join([ f'{x}{x}{y}' for x,y in zip(terminated_rsc_1,terminated_rsc_2)])

        return "".join(output)


if __name__ == '__main__':
    s = 'T'
    x = TurboCodeCoder([0,1,2,3,4,5,6]).encode_string(s)
    print(x[0::3])
    print(x[1::3])
    print(x[2::3])
