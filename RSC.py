class RSC:
    def __init__(self):
        self.mem = [0, 0]

    def push(self, input):
        ret = self.mem[1] ^ input
        self.mem[1] = self.mem[0]
        self.mem[0] = input

        return ret

    def terminate(self):
        return self.push(0)

