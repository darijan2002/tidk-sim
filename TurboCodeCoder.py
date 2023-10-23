from Coder import Coder
import numpy as np
import random


class RCS:
    mem = [0, 0]

    def push(self, bit):
        tmp = self.mem[0] ^ self.mem[1]
        input = bit ^ tmp
        ret = self.mem[1] ^ input

        self.mem[1] = self.mem[0]
        self.mem[0] = input

        return ret

    def terminate(self):
        return self.push(0)


# Turbo code coder
class TurboCodeCoder(Coder):
    interleaver = []

    def __init__(self):
        self.interleaver = [*range(7)]
        np.random.shuffle(self.interleaver)

    def encode_string(self, string):
        print(f'INTERLEAVER: {self.interleaver}')

        output = []
        for c in string:
            rcs1, rcs2 = RCS(), RCS()
            output.append("")
            to_bin = f'{ord(c):07b}'
            to_bin_i = ['']*7
            for i in range(7):
                to_bin_i[self.interleaver[i]] = to_bin[i]

            for b in range(len(to_bin)):
                output[-1] += to_bin[b]
                output[-1] += str(rcs1.push(int(to_bin[b])))
                output[-1] += str(rcs2.push(int(to_bin_i[b])))

            print(to_bin)
            print(to_bin_i)
            print("-" * 10)

        return "".join(output)


if __name__ == '__main__':
    x = TurboCodeCoder().encode_string('abcd')
    print(x)
