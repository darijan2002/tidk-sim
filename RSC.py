class RSC:
    def __init__(self):
        self.mem = [0, 0]

    def push(self, x):
        ret = self.mem[1] ^ x
        self.mem[1] = self.mem[0]
        self.mem[0] = ret

        return ret

    def terminate(self):
        ret = self.mem[1]
        self.mem[1] = self.mem[0]
        self.mem[0] = 0

        return ret

