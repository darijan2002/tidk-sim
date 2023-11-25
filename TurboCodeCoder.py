from Coder import Coder
import numpy as np

from RCS import RCS


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
    s = 'The quick brown fox jumps over the lazy dog'
    x = TurboCodeCoder().encode_string(s)
    print(x)
