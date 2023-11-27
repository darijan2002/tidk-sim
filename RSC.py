class RSC:
    def __init__(self):
        self.mem = [0, 0]

    def push(self, bit):
        tmp = self.mem[0] ^ self.mem[1]
        input = bit ^ tmp
        ret = self.mem[1] ^ input

        self.mem[1] = self.mem[0]
        self.mem[0] = input

        return ret

    def terminate(self):
        return self.push(0)

