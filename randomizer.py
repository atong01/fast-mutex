import numpy as np
from random import Random
from math import ceil, log
DEBUG = False
class Randomizer(object):
    def __init__(self, n, seed = None):
        """ The randomizer must know n to produce the correct distribution """
        self.seed = 42 if DEBUG else seed
        self.random = Random(self.seed)
        self.n = n
        self.logn = int(ceil(log(n,2)))

    def flip(self):
        return self.random.randint(0,1) == 1 

    def geometric(self, max_range = None):
        """ Implements a clipped geometric distribution.
        Note that np.random.geometric has range {1,2,...\infty}
        """
        val = np.random.geometric(p=0.5)
        if max_range is None:
            max_range = self.logn
        if val >= max_range:
            val = max_range 
        return val - 1

    def uniform(self):
        return self.random.randrange(self.n)
        
