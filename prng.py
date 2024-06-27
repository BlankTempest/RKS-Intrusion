class MersenneTwister:
    def __init__(self, seed=5489):
        self.w, self.n, self.m, self.r = 32, 624, 397, 31
        self.a = 0x9908B0DF
        self.u, self.d = 11, 0xFFFFFFFF
        self.s, self.b = 7, 0x9D2C5680
        self.t, self.c = 15, 0xEFC60000
        self.l = 18
        self.f = 1812433253

        self.lower_mask = (1 << self.r) - 1
        self.upper_mask = (~self.lower_mask) & self.d

        self.mt = [0] * self.n
        self.index = self.n + 1
        self.seed(seed)

    def seed(self, seed):
        self.mt[0] = seed
        for i in range(1, self.n):
            self.mt[i] = self.f * (self.mt[i-1] ^ (self.mt[i-1] >> (self.w - 2))) + i
            self.mt[i] &= self.d

    def twist(self):
        for i in range(self.n):
            x = (self.mt[i] & self.upper_mask) + (self.mt[(i+1) % self.n] & self.lower_mask)
            xA = x >> 1
            if x % 2 != 0:
                xA ^= self.a
            self.mt[i] = self.mt[(i + self.m) % self.n] ^ xA
        self.index = 0

    def random(self):
        if self.index >= self.n:
            if self.index > self.n:
                self.seed(5489) 
            self.twist()

        y = self.mt[self.index]
        y ^= (y >> self.u) & self.d
        y ^= (y << self.s) & self.b
        y ^= (y << self.t) & self.c
        y ^= y >> self.l

        self.index += 1
        return y & self.d
