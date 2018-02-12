from random import Random

DEBUG = True
DEBUG_SEED = 42

class Schedule(object):
    """ Initialize a process schedule.
    Args:
        n: (int) number of processes
        stype: (str) string representing how to generate schedule

    OBL type is an oblivious adversary, each process is scheduled chosen
    with replacement.
    SIN type is a process 0 only schedule

    """
    def __init__(self, n, stype = "OBL", seed = None):
        self.history = []
        self.num_p   = n
        self.stype   = stype
        if DEBUG:
            seed = 42
        self.random = Random(seed)

    def next(self):
        if self.stype == "OBL":
            next_p = self.random.randint(0, self.num_p - 1)
        if self.stype == "SIN":
            next_p = 0
        self.history.append(next_p)
        return next_p

    def next_n(self, length):
        return [self.next() for i in range(length)]

class Flipper(object):
    """ Initializes a flipper object, this holds the history of all coin flips.
    """
    def __init__(self, seed):
        self.history = []
        if DEBUG:
            seed = 42
        self.random = Random(seed)

    def next(self):
        flip = self.random.randint(0,1)
        self.history.append(flip)
        return flip

    def next_n(self, length):
        return [self.next() for i in range(length)]


class SharedMemory(object):
    """ Inits a shared memory consisting of a dictionary of registers """
    def __init__(self, registers):
        self.registers = registers

class RWMemory(SharedMemory):
    def __init__(self, registers):


class Process(object):
    def __init__(self):
        self.flipper = Flipper()
    
    def step():
        pass


class Algorithm(object):
    def __init__(self, n):
        self.n = n
        self.schedule = Schedule(n, stype = "OBL")


    def 

